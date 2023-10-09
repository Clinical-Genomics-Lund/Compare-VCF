import upsetplot
from matplotlib import pyplot as plt
import numpy as np


def write_variant_count_bars(variant_per_dataset: dict[str, set[str]], outpath: str):
    labels = []
    sizes = []
    for label, entries in variant_per_dataset.items():
        labels.append(label)
        sizes.append(len(entries))

    y_pos = np.arange(len(labels))

    plt.bar(y_pos, sizes, align="center", alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.ylabel("Number SNVs called")
    # plt.title("Number variants")
    plt.savefig(outpath)
    # plt.close()


def write_upset_chart(datasets: dict[str, set[str]], outpath: str):
    df = upsetplot.from_contents(datasets)
    upsetplot.plot(df)
    plt.savefig(outpath)
