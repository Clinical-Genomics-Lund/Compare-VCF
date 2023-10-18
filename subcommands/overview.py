from classes.vcf import VCF
import modules.annotations as annotations
import modules.charts as charts
import modules.tabletools as tabletools
import os


def overview_command(vcfs: list[VCF], contig: str | None, outdir: str):
    for ds in vcfs:
        ds.parse(None, contig)

    variant_keys_per_ds = {ds.label: ds.getVariantKeys() for ds in vcfs}
    charts.write_count_bars(variant_keys_per_ds, f"{outdir}/total_counts.png")

    charts.write_count_upset(variant_keys_per_ds, f"{outdir}/overlaps.png")
    os.makedirs(f"{outdir}/intersects", exist_ok=True)
    tabletools.write_vcf_intersects(variant_keys_per_ds, f"{outdir}/intersects")

    annotations.write_annotations_table(vcfs, f"{outdir}/annotations.tsv")

    charts.write_quality_histograms(vcfs, f"{outdir}/quality_overview.png")
