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
        "--scorekey", default=None, help="Study scoring present in INFO field"
    )
    args = parser.parse_args()
    return args
