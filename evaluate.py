import argparse

# import vcfpy
import sys
import upsetplot
from matplotlib import pyplot
from pysam import VariantFile
from modules.argparse import parse_arguments

# Draft command
# python evaluate.py --inputs data/231004_lund_wgs_snv/group.scored.chrnamed.autosomal.vcf.gz data/231004_nfcore_rd/giab_full_split_rmdup.chr.vcf.gz data/231006_nfcore_filtered_annotated/giab_full_ranked_snv.chr.dedup_info.vcf.gz --labels wgs nf_deep nf_sent --outdir testout

args = parse_arguments()

labels = []
if args.labels is not None:
    labels = args.labels
else:
    labels = args.inputs

datasets = dict()
for i in range(len(args.inputs)):
    label = labels[i]
    vcf_fp = args.inputs[i]
    print(f"Parsing: {label} ...")
    vcf_in = VariantFile(vcf_fp)
    # reader = vcfpy.Reader.from_path(
    #     vcf_fp,
    # )

    variants = set()
    for record in vcf_in.fetch("chr1"):
        # if record is None:
        #     print(f"No records found in path: {vcf_fp}")
        #     sys.exit(1)
        pos_name = f"{record.contig}:{record.pos}"
        variants.add(pos_name)

    datasets[label] = variants

print(datasets.keys())
df = upsetplot.from_contents(datasets)
print(df)
upsetplot.plot(df)

# Next steps:
# Also load the baseline
# Load the VCF files
# Extract position keys into a list of dictionaries
# Look into intersection and diagramming the intersects of these
