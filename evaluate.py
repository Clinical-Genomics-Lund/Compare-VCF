from modules.argparse import parse_arguments
import modules.charts as charts
from modules.dataset import Dataset
import warnings

# Upset chart library emits various warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Draft command
# python evaluate.py --inputs data/231004_lund_wgs_snv/group.scored.chrnamed.autosomal.vcf.gz data/231004_nfcore_rd/giab_full_split_rmdup.chr.vcf.gz data/231006_nfcore_filtered_annotated/giab_full_ranked_snv.chr.dedup_info.vcf.gz --labels wgs nf_deep nf_sent --outdir testout

args = parse_arguments()

labels = []
if args.labels is not None:
    labels = args.labels
else:
    labels = args.inputs


print(f"Inputs: {args.inputs} len: {len(args.inputs)}")

datasets: dict[str, Dataset] = dict()
for i in range(len(args.inputs)):
    label = labels[i]
    vcf_fp = args.inputs[i]
    print(f"Parsing: {label} with path {vcf_fp} ...")
    dataset = Dataset(label, vcf_fp)
    dataset.parse("chr1")
    datasets[label] = dataset

dataset_sets = dict()
for key, dataset in datasets.items():
    dataset_sets[key] = dataset._variants

# dataset_sets = {key: dataset._variants for (key, dataset) in datasets.items()}

for ds in datasets.values():
    print(str(ds))

charts.write_variant_count_bars(dataset_sets, f"{args.outdir}/total_counts.png")
charts.write_upset_chart(dataset_sets, f"{args.outdir}/overlaps.png")

for ds in datasets.values():
    if ds.hasRankScores():
        # Render histogram
        rank_scores = ds.getRankScores()

        zoom_in_threshold = 10
        charts.write_histograms(
            ds.label,
            rank_scores,
            zoom_in_threshold,
            f"{args.outdir}/{ds.label}_rank_histogram.png",
        )


# Also render scatter charts?


# if

# Retrieve comparisons from the R script
## Extract the rank score - Info RankScore

# RTG comparisons
