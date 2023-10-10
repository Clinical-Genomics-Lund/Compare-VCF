from modules.dataset import Dataset
import modules.util as util


# FIXME: Simplify this code. The data parsing prior to writing the heatmap should be made more elegant
def write_heatmaps(datasets: list[Dataset], outdir: str, top_n: int):
    nbr_datasets = len(datasets)
    if nbr_datasets >= 2:
        for i in range(nbr_datasets):
            for j in range(i + 1, nbr_datasets):
                ds1 = datasets[i]
                ds2 = datasets[j]

                # All scores
                shared_scores = util.get_scores_for_shared_variants(ds1, ds2, None)
                shared_scores_ds1 = [shared_score[1] for shared_score in shared_scores]
                shared_scores_ds2 = [shared_score[2] for shared_score in shared_scores]
                write_heatmap(
                    shared_scores_ds1,
                    shared_scores_ds2,
                    ds1.label,
                    ds2.label,
                    f"{outdir}/{ds1.label}_{ds2.label}_heat.png",
                )

                # Top N in first dataset
                shared_scores_top = util.get_scores_for_shared_variants(
                    ds1, ds2, top_n=top_n, top_from="first"
                )
                shared_scores_ds1_top = [
                    shared_score[1] for shared_score in shared_scores_top
                ]
                shared_scores_ds2_top = [
                    shared_score[2] for shared_score in shared_scores_top
                ]
                write_heatmap(
                    shared_scores_ds1_top,
                    shared_scores_ds2_top,
                    ds1.label,
                    ds2.label,
                    f"{outdir}/{ds1.label}_{ds2.label}_heat_{ds1.label}_top{top_n}.png",
                )

                # Top N in second dataset
                shared_scores_top = util.get_scores_for_shared_variants(
                    ds1, ds2, top_n=top_n, top_from="second"
                )
                shared_scores_ds1_top = [
                    shared_score[1] for shared_score in shared_scores_top
                ]
                shared_scores_ds2_top = [
                    shared_score[2] for shared_score in shared_scores_top
                ]
                write_heatmap(
                    shared_scores_ds1_top,
                    shared_scores_ds2_top,
                    ds1.label,
                    ds2.label,
                    f"{outdir}/{ds1.label}_{ds2.label}_heat_{ds2.label}_top{top_n}.png",
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
