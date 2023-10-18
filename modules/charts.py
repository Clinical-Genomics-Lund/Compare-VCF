import upsetplot
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import re

from classes.vcf import VCF


def write_count_bars(variant_per_dataset: dict[str, set[str]], outpath: str) -> None:
    labels = []
    sizes = []
    for label, entries in variant_per_dataset.items():
        labels.append(label)
        sizes.append(len(entries))

    y_pos = np.arange(len(labels))

    plt.bar(y_pos, sizes, align="center", alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.ylabel("Number SNVs called")
    plt.savefig(outpath)
    plt.close()


def write_count_upset(datasets: dict[str, set[str]], outpath: str) -> None:
    df = upsetplot.from_contents(datasets)
    upsetplot.plot(df)
    plt.savefig(outpath)
    plt.close()


def write_histogram_pair(
    label: str, values: list[int], top_n: int, outpath: str
) -> None:
    filtered_rank_scores = sorted(values, reverse=True)[0:top_n]
    # filtered_rank_scores = [value for value in values if value > top_n]
    plt.subplot(2, 1, 1)
    show_histogram(
        values,
        top_n=top_n,
        zoomed_in=False,
        label=label,
        xLabel=None,
        yLabel="Count",
    )
    plt.subplot(2, 1, 2)
    show_histogram(
        filtered_rank_scores,
        top_n=top_n,
        zoomed_in=True,
        label=None,
        xLabel=label,
        yLabel="Count",
    )
    plt.savefig(outpath)
    plt.close()


def show_histogram(
    values: list[int],
    top_n: int,
    zoomed_in: bool,
    label: str | None = None,
    xLabel: str | None = None,
    yLabel: str | None = None,
) -> None:
    sorted_values = sorted(values, reverse=True)
    df = pd.DataFrame({"Scores": sorted_values})

    if not zoomed_in:
        pass_thres = [
            "above" if i < top_n else "below" for i in range(len(sorted_values))
        ]
        df[f"Top {top_n}"] = pass_thres
    else:
        df[f"Top {top_n}"] = ["above" for _ in range(len(sorted_values))]

    hue_col = f"Top {top_n}"
    palette = {"above": "red", "below": "blue"}
    ax = sns.histplot(df, x="Scores", hue=hue_col, binwidth=1, palette=palette)
    ax.set(xlabel=xLabel, ylabel=yLabel, title=label)


def write_histograms(
    values_df: pd.DataFrame,
    outpath: str,
    title: str = "",
    figsize: tuple[int, int] = (15, 15),
    nbr_columns: int = 4,
):
    nbr_rows = len(values_df.columns) // nbr_columns + 1
    fig, axes = plt.subplots(nbr_rows, nbr_columns, figsize=figsize)
    ax = axes.flatten()

    for i, col in enumerate(values_df.columns):
        sns.histplot(values_df[col], ax=ax[i])
        # ax[i].set_title(col)

    if title != "":
        fig.suptitle(title)
    fig.tight_layout()

    plt.savefig(outpath)
    plt.close()


def write_quality_histograms(
    vcfs: list[VCF],
    outpath: str,
    figsize: tuple[int, int] = (15, 15),
    nbr_columns: int = 3,
):
    nbr_rows = len(vcfs) // nbr_columns + 1
    _fig, axes = plt.subplots(nbr_rows, nbr_columns, figsize=figsize)
    ax_arr = axes.flatten()
    for i, vcf in enumerate(vcfs):
        (quals, nbr_missing) = vcf.getQualities()

        # plt.hist(quals)
        sns.histplot(quals, ax=ax_arr[i]).set(
            title=f"{vcf.label} qualitites ({nbr_missing} missing)"
        )

    for i in range(len(vcfs), len(ax_arr)):
        ax_arr[i].set_axis_off()

    plt.savefig(outpath, bbox_inches="tight")
    plt.close()


# https://stackoverflow.com/questions/19366517/how-to-sort-a-list-containing-alphanumeric-values
def natural_sort_key(s):
    nsre = re.compile("([0-9]+)")
    return [int(text) if text.isdigit() else text.lower() for text in re.split(nsre, s)]


def write_snv_density_histograms(vcfs: list[VCF], outbase: str):
    for vcf in vcfs:
        write_snp_for_vcf(vcf, f"{outbase}/snp_density_{vcf.label}.png")


def write_snp_for_vcf(vcf: VCF, outpath: str):
    # Get used contigs
    # FIXME: In VCF class
    used_contigs = set()
    for variant in vcf.variants:
        used_contigs.add(variant.contig)
    used_contigs_list = sorted(list(used_contigs), key=natural_sort_key)

    # Extract positions per contig
    contig_to_pos_dict = dict()
    for contig in used_contigs_list:
        contig_positions = list()
        for var in vcf.getVariantPerContig(contig):
            snv_pos = var.pos
            contig_positions.append(snv_pos)
        contig_to_pos_dict[contig] = contig_positions

    # Actual plotting
    fig, axes = plt.subplots(len(contig_to_pos_dict), 1, figsize=(15, 40))
    for i, (contig, counts) in enumerate(contig_to_pos_dict.items()):
        # plt.subplot(4, 4, i)
        # plt.subplot(i)
        histplot = sns.histplot(counts, bins=200, ax=axes[i])
        histplot.set_title(contig)
        histplot.set(ylabel=None)
    # fig.tight_layout()
    plt.subplots_adjust(hspace=0.6)
    plt.savefig(outpath, bbox_inches="tight")
    plt.close()
