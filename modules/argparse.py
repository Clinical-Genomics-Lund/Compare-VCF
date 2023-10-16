import argparse
import os


def parse_arguments():
    parent_parser = argparse.ArgumentParser(
        description="Evaluate and compare set of VCF files"
    )

    subparsers = parent_parser.add_subparsers(
        help="Analyze rank models and their scores across VCF files",
        dest="subcommand",
        required=True,
    )
    add_overview_parser(subparsers)
    add_rank_model_parser(subparsers)

    args = parent_parser.parse_args()

    validate_inputs(args)

    return args


def add_overview_parser(subparsers):
    parser = subparsers.add_parser("overview")
    parser = subparsers.add_parser("overview")
    parser.add_argument(
        "-i", "--inputs", required=True, help="Input VCF files", nargs="+"
    )
    parser.add_argument("-o", "--outdir", required=True, help="Output folder")
    parser.add_argument("-l", "--labels", help="Label input VCFs", nargs="+")
    parser.add_argument(
        "--contig",
        default=None,
        help="Limit analysis to one contig",
    )
    parser.add_argument(
        "--annotations", help="Study scoring present in INFO field", action="store_true"
    )


def add_rank_model_parser(subparsers):
    parser = subparsers.add_parser("rankmodels")
    parser.add_argument(
        "-i", "--inputs", required=True, help="Input VCF files", nargs="+"
    )
    parser.add_argument("-o", "--outdir", required=True, help="Output folder")
    parser.add_argument("-l", "--labels", help="Label input VCFs", nargs="+")
    parser.add_argument(
        "--rankmodels",
        help="Optionally provide rank models corresponding to the provided inputs",
        nargs="+",
    )
    parser.add_argument(
        "--topn",
        default=20,
        help="Limit number of features included as 'top features'",
        type=int,
    )
    parser.add_argument("--scorekey", default="RankScore", help="Default score key")
    parser.add_argument(
        "--contig",
        default=None,
        help="Limit analysis to one contig",
    )


def validate_inputs(args):
    if args.subcommand == "rankmodels":
        if args.rankmodels is not None:
            if len(args.rankmodels) != len(args.inputs):
                raise ValueError(
                    f'Number of rankmodels must either be zero, or match the number of inputs, found {len(args.rankmodels)} rankmodels and {len(args.inputs)} inputs. Provide an empty string ("") if you want to compare a dataset without rank model'
                )

    if args.labels is not None:
        if len(args.labels) != len(args.inputs):
            raise ValueError(
                f"Number of labels must either be zero, or match the number of inputs, found {len(args.labels)} labels and {len(args.inputs)} inputs."
            )

    for input_fp in args.inputs:
        if not os.path.isfile(input_fp):
            raise ValueError(f"There is no file in {input_fp}")
