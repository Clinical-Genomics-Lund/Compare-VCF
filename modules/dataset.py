from pysam import VariantFile


RANK_SCORE = "RankScore"


class Variant:
    contig: str
    pos: int
    ref: str
    alt: str
    rankScore: int | None

    def getPosStr(self) -> str:
        return f"{self.contig}:{self.pos}"

    def getAlleleStr(self) -> str:
        return f"{self.ref}:{', '.join(list(self.alt))}"

    def getKey(self) -> str:
        return f"{self.getPosStr()}-{self.getAlleleStr()}"

    def __init__(self, contig, pos, ref, alt, rankScore):
        self.contig = contig
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.rankScore = rankScore


class Dataset:
    label: str
    variantNames: set[str]
    variants: list[Variant]
    _variantDict: dict[str, Variant]
    _filepath: str
    _rankScores: list[int]

    def __init__(self, label, filename):
        self.label = label
        self._filepath = filename
        self.variantNames = set()
        self._rankScores = list()
        self.variants = list()
        self._variantDict = dict()

    def hasRankScores(self) -> bool:
        return len(self._rankScores) > 0

    def getRankScores(self) -> list[int]:
        return self._rankScores

    def getVariantByKey(self, key: str) -> Variant | None:
        return self._variantDict.get(key)

    def parse(self, contigs=None) -> None:
        vcf_in = VariantFile(self._filepath)
        fh = vcf_in.fetch(contigs)
        has_rank_score = vcf_in.header.info.get(RANK_SCORE) is not None
        # rank_scores = list()
        for record in fh:
            pos_name = f"{record.contig}:{record.pos}"
            self.variantNames.add(pos_name)

            rank_score = None
            if has_rank_score:
                rank_score_cell = record.info.get(RANK_SCORE)
                rank_score = int(rank_score_cell[0].split(":")[-1])
                self._rankScores.append(rank_score)

            variant = Variant(
                record.contig, record.pos, record.ref, record.alts, rank_score
            )
            self.variants.append(variant)
            self._variantDict[variant.getKey()] = variant

        print(f"Number variants: {len(self.variantNames)}")

    def __str__(self):
        return f"{self.label}\t{len(self.variantNames)}\t{self._filepath}"
