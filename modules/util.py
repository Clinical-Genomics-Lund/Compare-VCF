from modules.dataset import Variant


def get_shared_ranks(variants1: list[Variant], variants2: list[Variant]) -> tuple[list[int], list[int]]|None:
    ds1_rank_per_pos = {
        var.getPosStr(): var.rankScore
        for var in variants1
        if var.rankScore is not None
    }
    ds2_rank_per_pos = {
        var.getPosStr(): var.rankScore
        for var in variants2
        if var.rankScore is not None
    }

    shared_keys = set(ds1_rank_per_pos.keys()).intersection(
        set(ds2_rank_per_pos.keys())
    )

    if len(shared_keys) == 0:
        return None

    ds1_ranks = list()
    ds2_ranks = list()
    for key in shared_keys:
        ds1_val = ds1_rank_per_pos[key]
        ds2_val = ds2_rank_per_pos[key]
        ds1_ranks.append(ds1_val)
        ds2_ranks.append(ds2_val)

    return (ds1_ranks, ds2_ranks)

