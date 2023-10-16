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
    rankmodels: list[RankModel],
):
    for vcf in vcfs:
        vcf.parse(SCOREKEY, contig)
    datasets_w_score = [ds for ds in vcfs if ds.hasScores()]
    for vcf in datasets_w_score:
        charts.write_histogram_pair(
            vcf.label,
            vcf.getScores(),
            topn,
            f"{outdir}/{vcf.label}_hist.png",
        )

    heatmap.write_freq_heatmaps(datasets_w_score, outdir, topn)

    if len(datasets_w_score) > 0:
        ranktable.write_score_table(
            datasets_w_score,
            topn,
            f"{outdir}/rank_table_top{topn}.tsv",
            rankmodels,
        )
