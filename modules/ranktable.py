import pandas as pd

from classes.vcf import VCF, Variant
from classes.rankmodel import RankModel


# Types
TopKeysPerDs = dict[str, set[str]]


# Constants
RANK_RESULT = "RankResult"


def write_score_table(
    vcfs: list[VCF], top_n: int, outpath: str, rank_models: list[RankModel] | None
):
    (all_top_keys, top_keys_per_ds) = get_top_scored_keys(vcfs, top_n)
    variant_column = "key"
    top_df = build_data_frame(
        vcfs, all_top_keys, top_keys_per_ds, top_n, variant_column
    )

    if rank_models is not None:
        for i, vcf in enumerate(vcfs):
            rank_categories_df = get_rank_categories_scores(
                vcf, rank_models[i], variant_column, list(top_df.index)
            )
            rank_categories_df.columns = [
                f"{vcf.label}_{col}" for col in rank_categories_df
            ]

            top_df = pd.concat([top_df, rank_categories_df], axis=1)

    top_df.to_csv(outpath, sep="\t", index=False)


def get_rank_categories_scores(
    dataset: VCF,
    rank_model: RankModel,
    variant_column: str,
    top_df_variant_keys: list[str] | None,
) -> pd.DataFrame:
    rank_result_dicts = list()

    target_keys = (
        top_df_variant_keys
        if top_df_variant_keys is not None
        else dataset.getVariantKeys()
    )

    for variant_key in target_keys:
        variant = dataset.getVariantByKey(variant_key)

        if variant is None:
            rank_result_dicts.append({variant_column: variant_key})
            continue

        variant_ranks_dict = get_variant_rank_categories_values(
            variant, rank_model.categories
        )
        variant_ranks_dict[variant_column] = variant_key  # type: ignore
        rank_result_dicts.append(variant_ranks_dict)

    dfs = [pd.DataFrame(d, index=[0]) for d in rank_result_dicts]
    comb = pd.concat(dfs)
    comb.set_index(variant_column, inplace=True)
    return comb


def get_variant_rank_categories_values(
    variant: Variant, rankscore_categories: list[str]
) -> dict[str, int]:
    single_rank_result_dict = dict()

    if variant is None:
        return single_rank_result_dict

    rank_result_strs = variant.info.get(RANK_RESULT)

    if rank_result_strs is not None:
        rank_result_str = rank_result_strs[0]

        values = [int(val) for val in rank_result_str.split("|")]
        for i, val in enumerate(values):
            single_rank_result_dict[rankscore_categories[i]] = val
    return single_rank_result_dict


def build_data_frame(
    datasets: list[VCF],
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
    ds: VCF, all_top_keys: set[str], ds_top_keys: set[str], top_n: int
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
    datasets: list[VCF], top_n: int
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
