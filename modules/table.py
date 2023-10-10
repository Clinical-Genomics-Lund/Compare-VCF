from modules.dataset import Dataset, Variant
import pandas as pd


def build_table(datasets: list[Dataset], top_n: int):
    print("Build table")

    dataset = datasets[1]
    variants = dataset.variants

    def sort_fn(variant: Variant):
        if variant.rankScore is not None:
            return variant.rankScore
        else:
            return -1

    sorted_variants = sorted(variants, key=sort_fn, reverse=True)
    top_sorted = sorted_variants[0:top_n]

    positions: list[str] = [var.getPosStr() for var in top_sorted]
    variant_strs: list[str] = [var.getAlleleStr() for var in top_sorted]
    scores: list[int | None] = [var.rankScore for var in top_sorted]

    top_df = pd.DataFrame({"pos": positions, "mut": variant_strs, "score": scores})

    print(top_df)
