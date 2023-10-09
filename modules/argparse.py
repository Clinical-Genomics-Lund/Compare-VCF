import argparse
import sys


def get_arguments():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Evaluate and compare set of VCF files"
    )
    parser.add_argument(
        "-i", "--inputs", required=True, help="Input VCF files", nargs="+"
    )
    parser.add_argument("-l", "--labels", help="Label input VCFs", nargs="+")
    parser.add_argument("-b", "--baseline", help="Reference VCF (for instance GIAB)")
    parser.add_argument("-o", "--outdir", required=True, help="Output folder")
    args = parser.parse_args()
    return args


def validate_argument(args):
    print("Finding input files")
    print(args.inputs)

    # FIXME: Move the input checking to a separate location
    if len(args.labels) > 0 and len(args.labels) != len(args.inputs):
        print("If labels are provided, the number need to match the number of inputs")
        print(f"Found {len(args.inputs)} inputs: {args.inputs}")
        print(f"Found {len(args.labels)} labels: {args.labels}")
        sys.exit(1)

    if args.labels is None:
        labels = [input_name.split("/")[-1] for input_name in args.inputs]
    else:
        labels = args.labels

    if len(set(labels)) != len(labels):
        print(f"Labels are not unique: {', '.join(labels)}")
        sys.exit(1)


def parse_arguments():
    args = get_arguments()
    validate_argument(args)
    return args
