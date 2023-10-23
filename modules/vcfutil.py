from classes.vcf import VCF


def get_scores_for_shared_variants(
    vcf1: VCF, vcf2: VCF, top_n: int | None, top_from: str = "first"
) -> list[tuple[str, int, int]]:
    """Given two arrays of variants, identify shared variants"""

    if top_n is None:
        all_keys = vcf1.getVariantKeys().union(vcf2.getVariantKeys())
    else:
        if top_from == "first":
            all_keys = vcf1.getTopScoredVariantKeys(top_n)
        elif top_from == "second":
            all_keys = vcf2.getTopScoredVariantKeys(top_n)
        else:
            raise ValueError(
                f"top_from should be either first or second, found {top_from}"
            )

    shared_scores = list()
    for key in all_keys:
        ds1_var = vcf1.getVariantByKey(key)
        ds2_var = vcf2.getVariantByKey(key)

        if ds1_var is None or ds2_var is None:
            continue

        if ds1_var.score is None or ds2_var.score is None:
            continue

        shared_score = (key, ds1_var.score, ds2_var.score)
        shared_scores.append(shared_score)

    return shared_scores
