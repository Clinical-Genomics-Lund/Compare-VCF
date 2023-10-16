from classes.vcf import VCF
from classes.rankmodel import RankModel
import modules.charts as charts
import modules.charts as charts
import modules.heatmap as heatmap
import modules.ranktable as ranktable
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


SCOREKEY = "RankScore"


def rankmodels_command(
    vcfs: list[VCF],
    contig: str | None,
    outdir: str,
    topn: int,
    rank_models: list[RankModel],
):
    for vcf in vcfs:
        vcf.parse(SCOREKEY, contig)
    for vcf in vcfs:
        charts.write_histogram_pair(
            vcf.label,
            vcf.getScores(),
            topn,
            f"{outdir}/{vcf.label}_hist.png",
        )

    heatmap.write_freq_heatmaps(vcfs, outdir, topn)
    ranktable.write_score_table(
        vcfs,
        topn,
        f"{outdir}/rank_table_top{topn}.tsv",
        rank_models,
    )

    # FIXME: Distribution histograms
    if rank_models is not None:
        for i, vcf in enumerate(vcfs):
            key_col_name = "key"
            scores_df = ranktable.get_rank_categories_scores(
                vcf, rank_models[i], key_col_name, None
            )
            charts.write_histograms(
                scores_df, f"{outdir}/{vcf.label}_rank_histograms.png", vcf.label
            )
            corr_df = scores_df.corr(method="spearman")

            # corr_df.style.background_gradient(cmap="coolwarm").format(precision=2)
            corr_df.to_excel(f"{outdir}/{vcf.label}_category_spearman.xlsx")

            sns.set_theme(style="white")
            mask = np.triu(np.ones_like(corr_df, dtype=bool))
            f, ax = plt.subplots(figsize=(11, 9))
            cmap = sns.diverging_palette(230, 20, as_cmap=True)
            sns.heatmap(
                corr_df,
                mask=mask,
                cmap=cmap,
                vmax=0.3,
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.5},
            )

            # fig = plt.figure(figsize=(15, 15))
            # plt.matshow(corr_df, fignum=fig.number)
            # plt.xticks(corr_df.columns)
            # plt.yticks(corr_df.columns)
            plt.title(f"Rank model categories Spearman correlation", fontsize=16)
            f.tight_layout()
            plt.savefig(f"{outdir}/{vcf.label}_category_spearman.png")
            plt.close()

    # FIXME: Correlation scores matrix
