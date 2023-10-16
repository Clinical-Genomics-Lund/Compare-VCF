import warnings
import os

from modules.argparse import parse_arguments
import modules.charts as charts
import modules.heatmap as heatmap
import modules.ranktable as ranktable
import modules.annotations as annotations
from modules.dataset import Dataset

# Upset chart library emits various warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    args = parse_arguments()

    print("In main!")
    print(args.command)

    # labels = get_labels(args)
    # datasets = setup_datasets(args.inputs, labels, args.scorekey, args.contig)
    # datasets_w_score = [ds for ds in datasets if ds.hasScores()]
    # variant_keys_per_ds = {ds.label: ds.getVariantKeys() for ds in datasets}
    # os.makedirs(args.outdir, exist_ok=True)

    # charts.write_count_bars(variant_keys_per_ds, f"{args.outdir}/total_counts.png")
    # charts.write_count_upset(variant_keys_per_ds, f"{args.outdir}/overlaps.png")

    # for ds in datasets_w_score:
    #     charts.write_histogram_pair(
    #         ds.label,
    #         ds.getScores(),
    #         args.topn,
    #         f"{args.outdir}/{ds.label}_hist.png",
    #     )

    # heatmap.write_freq_heatmaps(datasets_w_score, args.outdir, args.topn)

    # if len(datasets_w_score) > 0:
    #     ranktable.write_score_table(
    #         datasets_w_score,
    #         args.topn,
    #         f"{args.outdir}/rank_table_top{args.topn}.tsv",
    #         args.rankmodels,
    #     )

    # if args.annotations:
    #     annotations.write_annotations_table(datasets, f"{args.outdir}/annotations.tsv")


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
        dataset = Dataset(label, vcf_fp)
        dataset.parse(score_key, contig)
        datasets.append(dataset)
    return datasets


if __name__ == "__main__":
    main()
