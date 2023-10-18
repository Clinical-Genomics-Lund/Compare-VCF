import upsetplot
import re
import pandas as pd

import modules.util as util


def write_vcf_intersects(datasets: dict[str, set[str]], outdir: str) -> None:
    df_nested_index = upsetplot.from_contents(datasets)

    contrast_df = df_nested_index.reset_index()
    all_keys = list(datasets.keys())
    combinations = util.get_all_combinations(all_keys)
    for comb in combinations:
        out_df = make_comb_df(contrast_df, comb)

        out_label = "_".join(list(comb))
        out_path = f"{outdir}/{out_label}.csv"
        out_df.to_csv(out_path, index=False)


def make_comb_df(df: pd.DataFrame, col_comb: list[str]) -> pd.DataFrame:
    true_rows = df[list(col_comb)].all(axis=1)
    keys = list(df.loc[true_rows, "id"])
    split_keys = [re.split("[-:]", myid) for myid in keys]
    out_df = pd.DataFrame(split_keys, columns=["Chr", "Position", "Ref", "Var"])
    out_df[["Position"]] = out_df[["Position"]].astype(int)
    out_df.sort_values(by=["Chr", "Position"], inplace=True)
    return out_df
