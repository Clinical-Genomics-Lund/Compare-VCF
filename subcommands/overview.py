from classes.vcf import VCF
import modules.annotations as annotations
import modules.charts as charts


def overview_command(datasets: list[VCF], contig: str | None, outdir: str):
    for ds in datasets:
        ds.parse(None, contig)
    variant_keys_per_ds = {ds.label: ds.getVariantKeys() for ds in datasets}
    charts.write_count_bars(variant_keys_per_ds, f"{outdir}/total_counts.png")
    charts.write_count_upset(variant_keys_per_ds, f"{outdir}/overlaps.png")
    annotations.write_annotations_table(datasets, f"{outdir}/annotations.tsv")
