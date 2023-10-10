from modules.argparse import parse_arguments
import modules.charts as charts
import modules.table as table
from modules.dataset import Dataset
import warnings
import numpy as np

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
    dataset_sets[key] = dataset.variantNames

# dataset_sets = {key: dataset._variants for (key, dataset) in datasets.items()}

for ds in datasets.values():
    print(str(ds))

charts.write_variant_count_bars(dataset_sets, f"{args.outdir}/total_counts.png")
charts.write_upset_chart(dataset_sets, f"{args.outdir}/overlaps.png")

for ds in datasets.values():
    if not ds.hasRankScores():
        continue
    rank_scores = ds.getRankScores()
    zoom_in_threshold = 10
    charts.write_histograms(
        ds.label,
        rank_scores,
        zoom_in_threshold,
        f"{args.outdir}/{ds.label}_rank_histogram.png",
    )

# FIXME: A bit more tricky - we need to match rank scores on positions
# Let's start with doing it the ugly way, and then think about refactoring
nbr_datasets = len(datasets.values())
dataset_list = list(datasets.values())
if nbr_datasets >= 2:
    for i in range(nbr_datasets):
        for j in range(i + 1, nbr_datasets):
            ds1 = dataset_list[i]
            ds2 = dataset_list[j]

            print("-------")
            print([var.rankScore for i, var in enumerate(ds1.variants) if i < 10])
            print([var.rankScore for i, var in enumerate(ds2.variants) if i < 10])
            print("-------")

            ds1_rank_per_pos = {
                var.getPosStr(): var.rankScore
                for var in ds1.variants
                if var.rankScore is not None
            }
            ds2_rank_per_pos = {
                var.getPosStr(): var.rankScore
                for var in ds2.variants
                if var.rankScore is not None
            }

            shared_keys = set(ds1_rank_per_pos.keys()).intersection(
                set(ds2_rank_per_pos.keys())
            )

            if len(shared_keys) == 0:
                continue

            ds1_ranks = list()
            ds2_ranks = list()
            for key in shared_keys:
                ds1_val = ds1_rank_per_pos[key]
                ds2_val = ds2_rank_per_pos[key]
                ds1_ranks.append(ds1_val)
                ds2_ranks.append(ds2_val)

            print(f"First scatter {ds1_ranks[0:10]}")
            print(f"Second scatter {ds2_ranks[0:10]}")


            charts.write_rank_scatter(
                ds1_ranks,
                ds2_ranks,
                ds1.label,
                ds2.label,
                f"{args.outdir}/{ds1.label}_{ds2.label}_ranks.png",
            )


table.build_table()



# Next:
# Building the table
# RTG comparisons
