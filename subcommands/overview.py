from classes.vcf import VCF
import modules.annotations as annotations
import modules.charts as charts
import pandas as pd


def overview_command(vcfs: list[VCF], contig: str | None, outdir: str):
    for ds in vcfs:
        ds.parse(None, contig)

    variant_keys_per_ds = {ds.label: ds.getVariantKeys() for ds in vcfs}
    # charts.write_count_bars(variant_keys_per_ds, f"{outdir}/total_counts.png")
    # charts.write_count_upset(variant_keys_per_ds, f"{outdir}/overlaps.png")
    # annotations.write_annotations_table(vcfs, f"{outdir}/annotations.tsv")

    # FIXME: New chart, annotation quality histograms
    # charts.write_histograms()
    charts.write_quality_histograms(vcfs, f"{outdir}/quality_overview.png")


# def prepare_quality_df(vcfs: list[VCF]) -> dict[str, pd.DataFrame]:
#     my_dict = dict()
#     for vcf in vcfs:
