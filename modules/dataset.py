from pysam import VariantFile


RANK_SCORE = "RankScore"


class Dataset:
    label: str
    _filepath: str
    _variants: set[str]
    _rankScores: list[int]

    def __init__(self, label, filename):
        self.label = label
        self._filepath = filename
        self._variants = set()

    def hasRankScores(self) -> bool:
        return len(self._rankScores) > 0

    def getRankScores(self) -> list[int]:
        return self._rankScores

    def parse(self, contigs=None) -> None:
        print(f">>> file path {self._filepath}")
        vcf_in = VariantFile(self._filepath)
        fh = vcf_in.fetch(contigs)
        has_rank_score = vcf_in.header.info.get(RANK_SCORE) is not None
        rank_scores = list()
        for record in fh:
            pos_name = f"{record.contig}:{record.pos}"
            self._variants.add(pos_name)

            if has_rank_score:
                rank_score_cell = record.info.get(RANK_SCORE)
                rank_score = rank_score_cell[0].split(":")[-1]
                rank_scores.append(int(rank_score))
        self._rankScores = rank_scores

        print(f"Number variants: {len(self._variants)}")

    def __str__(self):
        return f"{self.label}\t{len(self._variants)}\t{self._filepath}"
