import argparse

# Parse arguments
parser = argparse.ArgumentParser(description="Evaluate and compare set of VCF files")
parser.add_argument("-i", "--inputs", required=True, help="Input VCF files", nargs="+")
parser.add_argument("-l", "--inputLabels", help="Label input VCFs", nargs="+")
parser.add_argument("-b", "--baseline", help="Reference VCF (for instance GIAB)")
parser.add_argument("-o", "--outDir", required=True, help="Output folder")
args = parser.parse_args()

print("Finding input files")
print(args.inputs)
