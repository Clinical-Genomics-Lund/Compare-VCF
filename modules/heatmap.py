from modules.dataset import Dataset
import modules.util as util
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def write_freq_heatmaps(datasets: list[Dataset], outdir: str, top_n: int):
    nbr_datasets = len(datasets)
    if nbr_datasets >= 2:
        for i in range(nbr_datasets):
            for j in range(i + 1, nbr_datasets):
                ds1 = datasets[i]
                ds2 = datasets[j]
                write_heatmap_from_datasets(ds1, ds2, outdir, None)
                write_heatmap_from_datasets(ds1, ds2, outdir, top_n, top_from="first")
                write_heatmap_from_datasets(ds1, ds2, outdir, top_n, top_from="second")


def write_heatmap_from_datasets(
    ds1: Dataset, ds2: Dataset, outdir: str, top_n: int | None, top_from: str = "first"
):
    shared_scores = util.get_scores_for_shared_variants(ds1, ds2, top_n, top_from)
    shared_scores_ds1 = [shared_score[1] for shared_score in shared_scores]
    shared_scores_ds2 = [shared_score[2] for shared_score in shared_scores]
    if top_n is None:
        out_path = f"{outdir}/{ds1.label}_{ds2.label}_heat.png"
    else:
        target_label = ds1.label if top_from == "first" else ds2.label
        out_path = f"{outdir}/{ds1.label}_{target_label}_{top_n}_heat.png"

    write_heatmap(
        shared_scores_ds1,
        shared_scores_ds2,
        ds1.label,
        ds2.label,
        out_path,
    )


def write_heatmap(
    scores_ds1: list[int],
    scores_ds2: list[int],
    xLabel: str,
    yLabel: str,
    outpath: str,
) -> None:
    if len(scores_ds1) != len(scores_ds2):
        raise ValueError(
            f"Length of value arrays expected to be the same, found {len(scores_ds1)} and {len(scores_ds2)}"
        )
    corr_coef = np.corrcoef(scores_ds1, scores_ds2)

    df = pd.DataFrame({"dataset1": scores_ds1, "dataset2": scores_ds2})
    ax = sns.displot(
        df,
        x="dataset1",
        y="dataset2",
        binwidth=1,
        cbar=True,
        alpha=1,
    )
    ax.set(
        title=f"{xLabel} vs {yLabel} (corr: {round(corr_coef[0][1], 2)})",
        xlabel=xLabel,
        ylabel=yLabel,
    )
    plt.savefig(outpath, bbox_inches="tight")
    plt.close()
