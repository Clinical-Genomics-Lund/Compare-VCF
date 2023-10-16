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

    # FIXME: Correlation scores matrix
