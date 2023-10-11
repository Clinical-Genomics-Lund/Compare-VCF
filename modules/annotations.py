from modules.dataset import Dataset
import pandas as pd


def write_annotations_table(datasets: list[Dataset], filepath: str):
    # # for ds in datasets:
    # label1 = datasets[0].label
    # annot1_dict = {"CADD": 3, "VCF": None, "INDEL": 2}
    # annot1_df = pd.DataFrame(annot1_dict)
    # label2 = datasets[0].label
    # annot2_dict = {"CADD": 2, "VCF": None, "INDEL": 2}
    # annot2_df = pd.DataFrame(annot2_dict)

    annot_dicts = []
    for ds in datasets:
        annot_dict = dict()
        variants = ds.variants
        annot_dict["sample"] = ds.label
        for variant in variants:
            for info_key, info_value in variant.info.items():
                if annot_dict.get(info_key) is None:
                    annot_dict[info_key] = [0]
                annot_dict[info_key][0] += 1
        annot_dicts.append(annot_dict)

    # Seems secessary to convert the dict into pandas Data Frame?
    # annot_dicts_lists = {item[0]: [item[1]] for item in annot_dicts}
    annot_dfs = [pd.DataFrame(annot_dict) for annot_dict in annot_dicts]
    combined_df = pd.concat(annot_dfs)

    # label3 = datasets[0].label
    # annot3_dict = {"CADD": 0, "VCF": "X", "INDEL": 5}
    # annot3_df = pd.DataFrame(annot1_dict)

    # out_df = pd.DataFrame(
    #     {
    #         "sample": ["ds1", "ds2"],
    #         "CADD": [3, 4],
    #         "VCF": [None, "C"],
    #         "INDEL": [2, None],
    #     }
    # )
    combined_df.to_csv(filepath, sep="\t", index=False)
