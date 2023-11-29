from classes.vcf import VCF
from classes.rankmodel import RankModel
import modules.charts as charts
import modules.charts as charts
import modules.heatmap as heatmap
import modules.ranktable as ranktable


SCOREKEY = "RankScore"


def rankmodels_command(
    vcfs: list[VCF],
    contig: str | None,
    outdir: str,
    topn: int,
    rank_models: list[RankModel],
    true_variants: set[str] | None,
):
    print("Parsing VCFs")
    for vcf in vcfs:
        print(f"Parsing: {vcf.label}")
        vcf.parse(SCOREKEY, contig)
    print("Writing histogram pairs")
    for vcf in vcfs:
        charts.write_histogram_pair(
            vcf.label,
            vcf.getScores(),
            topn,
            f"{outdir}/{vcf.label}_hist.png",
        )

    print("Writing frequency heatmaps")
    heatmap.write_freq_heatmaps(vcfs, outdir, topn)
    print("Writing score table")
    ranktable.write_score_table(
        vcfs,
        topn,
        f"{outdir}/rank_table_top{topn}.tsv",
        rank_models,
        true_variants,
    )

    print("Rank model details")
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
            corr_df.to_excel(f"{outdir}/{vcf.label}_category_spearman.xlsx")
            charts.write_corr_heatmap(
                corr_df, f"{outdir}/{vcf.label}_category_spearman.png"
            )

            topn_scores_df = scores_df.sort_values("score", ascending=False).head(topn)
            charts.write_histograms(
                topn_scores_df,
                f"{outdir}/{vcf.label}_top{topn}_rank_histograms.png",
                vcf.label,
            )
            topn_corr_df = topn_scores_df.corr(method="spearman")
            topn_corr_df.to_excel(
                f"{outdir}/{vcf.label}_top{topn}_category_spearman.xlsx"
            )
            charts.write_corr_heatmap(
                topn_corr_df, f"{outdir}/{vcf.label}_top{topn}_category_spearman.png"
            )
