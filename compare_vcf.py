import warnings
import os

from classes.rankmodel import RankModel
from classes.vcf import VCF
from subcommands.overview import overview_command
from subcommands.rankmodels import rankmodels_command
from modules.argparse import parse_arguments

# Upset chart library emits various warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    args = parse_arguments()

    labels = get_labels(args)
    datasets = setup_datasets(args.inputs, labels)
    os.makedirs(args.outdir, exist_ok=True)

    if args.subcommand == "overview":
        overview_command(
            datasets,
            args.contig,
            args.outdir,
            skip_density_histogram=args.skip_snp_density_histogram,
        )

    elif args.subcommand == "rankmodels":
        if args.rankmodels is not None:
            rankmodels = [RankModel(path) for path in args.rankmodels]
        else:
            rankmodels = []

        rankmodels_command(datasets, args.contig, args.outdir, args.topn, rankmodels)

    else:
        # FIXME: Programatically calculate
        raise ValueError("Invalid subcommand, valid are: overview, rankmodels")


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
) -> list[VCF]:
    datasets = list()
    for i in range(len(input_paths)):
        label = labels[i]
        vcf_fp = input_paths[i]
        vcf = VCF(label, vcf_fp)
        datasets.append(vcf)
    return datasets


if __name__ == "__main__":
    main()
