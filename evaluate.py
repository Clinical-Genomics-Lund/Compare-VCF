from modules.argparse import parse_arguments
import modules.charts as charts
import modules.table as table
from modules.dataset import Dataset
import warnings
import modules.util as util

# Upset chart library emits various warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    args = parse_arguments()

    labels = get_labels(args)

    datasets = setup_datasets(args.inputs, labels, args.scorekey, args.contig)
    variant_keys_per_ds = {ds.label: ds.getVariantKeys() for ds in datasets}

    charts.write_variant_count_bars(
        variant_keys_per_ds, f"{args.outdir}/total_counts.png"
    )
    charts.write_upset_chart(variant_keys_per_ds, f"{args.outdir}/overlaps.png")

    generate_histograms(list(datasets), args.outdir)
    generate_heatmaps(list(datasets), args.outdir)
    table.build_table(list(datasets), args.topn, f"{args.outdir}/table.tsv")


def get_labels(args) -> list[str]:
    labels = []
    if args.labels is not None:
        labels = args.labels
    else:
        labels = args.inputs
    return labels


def setup_datasets(
    input_paths: list[str],
    labels: list[str],
    score_key: str | None = None,
    contig: str | None = None,
) -> list[Dataset]:
    datasets = list()
    for i in range(len(input_paths)):
        label = labels[i]
        vcf_fp = input_paths[i]
        print(f"Parsing: {label} with path {vcf_fp} ...")
        dataset = Dataset(label, vcf_fp)
        dataset.parse(score_key, contig)
        datasets.append(dataset)
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
                charts.write_rank_heatmap(
                    ranks1,
                    ranks2,
                    ds1.label,
                    ds2.label,
                    f"{outdir}/{ds1.label}_{ds2.label}_ranks.png",
                )


if __name__ == "__main__":
    main()
