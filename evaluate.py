from modules.argparse import parse_arguments
import modules.charts as charts
import modules.table as table
from modules.dataset import Dataset
import warnings
import numpy as np
import modules.util as util

# Upset chart library emits various warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Draft command
# python evaluate.py --inputs data/231004_lund_wgs_snv/group.scored.chrnamed.autosomal.vcf.gz data/231004_nfcore_rd/giab_full_split_rmdup.chr.vcf.gz data/231006_nfcore_filtered_annotated/giab_full_ranked_snv.chr.dedup_info.vcf.gz --labels wgs nf_deep nf_sent --outdir testout

def main():

    args = parse_arguments()

    labels = []
    if args.labels is not None:
        labels = args.labels
    else:
        labels = args.inputs

    datasets = setup_datasets(args.inputs, labels, "chr1")
    dataset_sets = dict()
    for key, dataset in datasets.items():
        dataset_sets[key] = dataset.variantNames

    # charts.write_variant_count_bars(dataset_sets, f"{args.outdir}/total_counts.png")
    # charts.write_upset_chart(dataset_sets, f"{args.outdir}/overlaps.png")

    # generate_histograms(list(datasets.values()), args.outdir)
    # generate_heatmaps(list(datasets.values()), args.outdir)

    table.build_table(list(datasets.values()), 20)


def setup_datasets(input_paths: list[str], labels: list[str], contig: str|None = None) -> dict[str, Dataset]:
    datasets = dict()
    for i in range(len(input_paths)):
        label = labels[i]
        vcf_fp = input_paths[i]
        print(f"Parsing: {label} with path {vcf_fp} ...")
        dataset = Dataset(label, vcf_fp)
        dataset.parse(contig)
        datasets[label] = dataset
    return datasets



def generate_histograms(datasets: list[Dataset], outdir: str):
    for ds in datasets:
        if not ds.hasRankScores():
            continue
        rank_scores = ds.getRankScores()
        zoom_in_threshold = 10
        charts.write_histograms(
            ds.label,
            rank_scores,
            zoom_in_threshold,
            f"{outdir}/{ds.label}_rank_histogram.png",
        )


def generate_heatmaps(datasets: list[Dataset], outdir: str):
    # FIXME: A bit more tricky - we need to match rank scores on positions
    # Let's start with doing it the ugly way, and then think about refactoring
    nbr_datasets = len(datasets)
    dataset_list = list(datasets)
    if nbr_datasets >= 2:
        for i in range(nbr_datasets):
            for j in range(i + 1, nbr_datasets):
                ds1 = dataset_list[i]
                ds2 = dataset_list[j]

                shared_ranks = util.get_shared_ranks(ds1.variants, ds2.variants)
                if shared_ranks is None:
                    continue
                (ranks1, ranks2) = shared_ranks
                charts.write_rank_scatter(
                    ranks1,
                    ranks2,
                    ds1.label,
                    ds2.label,
                    f"{outdir}/{ds1.label}_{ds2.label}_ranks.png",
                )


# Next:
# Building the table
# RTG comparisons

if __name__ == "__main__":
    main()
