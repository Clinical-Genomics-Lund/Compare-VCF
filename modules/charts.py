import upsetplot
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


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


