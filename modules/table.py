import pandas as pd

from modules.dataset import Dataset, Variant
import modules.util as util


TopKeysPerDs = dict[str, set[str]]


def write_score_table(
    datasets: list[Dataset], top_n: int, outpath: str, rankmodel_paths: list[str] | None
):
    (all_top_keys, top_keys_per_ds) = get_top_scored_keys(datasets, top_n)
    variant_key = "key"
    top_df = build_data_frame(
        datasets, all_top_keys, top_keys_per_ds, top_n, variant_key
    )

    # # FIXME: Refactor
    # if rankmodel_paths is not None:
    #     config = ConfigObj(rankmodel_paths[0])
    #     categories_section = config["Categories"]
    #     categories_keys = categories_section.keys()  # type: ignore
    #     print(categories_keys)

    # FIXME: Cleanup in this part
    # Some function extraction
    # Some simplification
    for i, ds in enumerate(datasets):
        rank_result_strings = list()
        rank_result_dicts = list()

        # FIXME: Handle that this isn't always present
        rankscore_categories = util.get_rankscore_categories(rankmodel_paths[i])

        for key in top_df.index:
            variant = ds.getVariantByKey(key)
            single_rank_result_dict = {"key": key}
            if variant is None:
                rank_result_strings.append(None)
                rank_result_dicts.append(single_rank_result_dict)
                continue

            rank_result_strs = variant.info.get("RankResult")

            if rank_result_strs is not None:
                rank_result_str = rank_result_strs[0]
                rank_result_strings.append(rank_result_str)

                values = [int(val) for val in rank_result_str.split("|")]
                for i, val in enumerate(values):
                    single_rank_result_dict[
                        f"{ds.label}_{rankscore_categories[i]}"
                    ] = val
                rank_result_dicts.append(single_rank_result_dict)
            else:
                rank_result_strings.append(None)
                rank_result_dicts.append(single_rank_result_dict)

        # rank_result_values.append(single_rank_result_dict)

        dfs = [pd.DataFrame(d, index=[0]) for d in rank_result_dicts]
        comb = pd.concat(dfs)
        comb.set_index(variant_key, inplace=True)

        top_df[f"{ds.label}_rank_string"] = rank_result_strings
        top_df = pd.concat([top_df, comb], axis=1)

    top_df.to_csv(outpath, sep="\t", index=False)


def build_data_frame(
    datasets: list[Dataset],
    all_top_keys: set[str],
    top_keys_per_ds: TopKeysPerDs,
    top_n: int,
    variant_key: str,
) -> pd.DataFrame:
    table_dict: dict[str, list[bool | int | str]] = dict()
    table_dict[variant_key] = list(all_top_keys)
    for ds in datasets:
        ds_top_keys = top_keys_per_ds[ds.label]
        ds_cols = get_dataset_columns(ds, all_top_keys, ds_top_keys, top_n)

        for key, col in ds_cols.items():
            assert (
                key not in table_dict.keys()
            ), f"{key} already present in table_dict, among keys: {', '.join(list(table_dict.keys()))}"
            table_dict[key] = col

    top_df = pd.DataFrame(table_dict)
    score_labels = [f"{ds.label}_score" for ds in datasets]
    top_df.sort_values(by=score_labels, inplace=True, ascending=False)
    top_df.set_index(variant_key, inplace=True)
    return top_df


def get_dataset_columns(
    ds: Dataset, all_top_keys: set[str], ds_top_keys: set[str], top_n: int
) -> dict[str, list[bool | int | str]]:
    col_dict = dict()
    # FIXME: Avoid hard-coding, lift this up from this function
    present_label = f"{ds.label}_present"
    col_dict[present_label] = [
        ds.getVariantByKey(key) is not None for key in all_top_keys
    ]
    top_n_label = f"{ds.label}_top{top_n}"
    col_dict[top_n_label] = [key in ds_top_keys for key in all_top_keys]
    score_label = f"{ds.label}_score"
    col_dict[score_label] = [ds.getScoreByKey(key) for key in all_top_keys]
    return col_dict


def get_top_scored_keys(
    datasets: list[Dataset], top_n: int
) -> tuple[set[str], TopKeysPerDs]:
    all_top_keys = set()
    top_keys_per_ds: dict[str, set[str]] = dict()

    def sort_fn(variant: Variant):
        if variant.score is not None:
            return variant.score
        else:
            return -1

    for ds in datasets:
        variants = ds.variants
        sorted_variants = sorted(variants, key=sort_fn, reverse=True)
        top_variants = sorted_variants[0:top_n]
        var_keys = [var.getKey() for var in top_variants]
        all_top_keys.update(var_keys)
        top_keys_per_ds[ds.label] = set(var_keys)
    return (all_top_keys, top_keys_per_ds)
