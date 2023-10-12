import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Evaluate and compare set of VCF files"
    )
    parser.add_argument(
        "-i", "--inputs", required=True, help="Input VCF files", nargs="+"
    )
    parser.add_argument("-l", "--labels", help="Label input VCFs", nargs="+")
    parser.add_argument("-b", "--baseline", help="Reference VCF (for instance GIAB)")
    parser.add_argument("-o", "--outdir", required=True, help="Output folder")
    parser.add_argument(
        "--contig",
        default=None,
        help="Limit analysis to one contig",
    )
    parser.add_argument(
        "--topn",
        default=20,
        help="Limit number of features included as 'top features'",
        type=int,
    )
    parser.add_argument(
        "--scorekey", default="RankScore", help="Study scoring present in INFO field"
    )
    parser.add_argument(
        "--annotations", help="Study scoring present in INFO field", action="store_true"
    )

    parser.add_argument(
        "--rankmodels",
        help="Optionally provide rank models corresponding to the provided inputs",
        nargs="+",
    )

    args = parser.parse_args()
    validate_inputs(args)
    return args


def validate_inputs(args):
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
