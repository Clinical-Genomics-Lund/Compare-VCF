import pandas as pd

from modules.dataset import Dataset


def write_annotations_table(datasets: list[Dataset], filepath: str):
    annot_dicts = []
    for ds in datasets:
        annot_dict = dict()
        variants = ds.variants
        annot_dict["sample"] = ds.label

        nbr_annots = 0
        nbr_csqs = 0

        for variant in variants:
            for info_key, info_value in variant.info.items():
                if annot_dict.get(info_key) is None:
                    annot_dict[info_key] = [0, info_value]
                    nbr_annots += 1
                annot_dict[info_key][0] += 1
            for csq_key, csq_value in variant.getCSQ().items():
                dict_key = f"csq_{csq_key}"
                if annot_dict.get(dict_key) is None:
                    annot_dict[dict_key] = [0, csq_value]
                    nbr_csqs += 1
                annot_dict[dict_key][0] += 1

        annot_dicts.append(annot_dict)

    annot_dicts_with_counts = [d for d in annot_dicts if len(d.keys()) > 1]

    # Seems secessary to convert the dict into pandas Data Frame?
    # annot_dicts_lists = {item[0]: [item[1]] for item in annot_dicts}
    annot_dfs = [pd.DataFrame(annot_dict) for annot_dict in annot_dicts_with_counts]
    combined_df = pd.concat(annot_dfs)
    combined_df.set_index("sample").transpose().to_csv(filepath, sep="\t")
