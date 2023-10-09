import upsetplot
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def write_variant_count_bars(
    variant_per_dataset: dict[str, set[str]], outpath: str
) -> None:
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


def write_upset_chart(datasets: dict[str, set[str]], outpath: str) -> None:
    df = upsetplot.from_contents(datasets)
    upsetplot.plot(df)
    plt.savefig(outpath)
    plt.close()


def write_histograms(
    label: str, rank_scores: list[int], threshold: int, outpath: str
) -> None:
    filtered_rank_scores = [score for score in rank_scores if score > threshold]
    plt.subplot(2, 1, 1)
    show_histogram(
        rank_scores, label=label, xLabel=None, yLabel="Count", colorThreshold=threshold
    )
    plt.subplot(2, 1, 2)
    show_histogram(
        filtered_rank_scores,
        label=None,
        xLabel=label,
        yLabel="Count",
        colorThreshold=None,
    )
    plt.savefig(outpath)
    plt.close()


def show_histogram(
    rank_scores: list[int],
    label: str | None = None,
    xLabel: str | None = None,
    yLabel: str | None = None,
    colorThreshold: int | None = None,
) -> None:
    print(f"Writing histogram... {len(rank_scores)} data points")

    df = pd.DataFrame({"Scores": rank_scores})
    if colorThreshold is not None:
        color_categories = [
            "above" if score > colorThreshold else "below" for score in rank_scores
        ]
        df["Threshold"] = color_categories

    hue_col = "Threshold" if colorThreshold else None
    ax = sns.histplot(df, x="Scores", hue=hue_col, binwidth=1)
    ax.set(xlabel=xLabel, ylabel=yLabel, title=label)

    # plt.hist(rank_scores, bins=bins)
    # if label is not None:
    #     plt.title(label)
    # if xLabel is not None:
    #     plt.xlabel("Rank")
    # if yLabel is not None:
    #     plt.ylabel("Count")
    # plt.savefig(outpath)
    # plt.close()
