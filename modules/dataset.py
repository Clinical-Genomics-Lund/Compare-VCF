from pysam import VariantFile, VariantHeader
from logging import debug


class Variant:
    key: str
    contig: str
    pos: int
    ref: str | None
    alt: tuple[str, ...] | None
    score: int | None
    info: dict[str, tuple[str]]
    header: VariantHeader

    def getPosStr(self) -> str:
        return f"{self.contig}:{self.pos}"

    def getAlleleStr(self) -> str:
        if self.alt is None:
            return ""
        return f"{self.ref}:{', '.join(list(self.alt))}"

    def getKey(self) -> str:
        return f"{self.getPosStr()}-{self.getAlleleStr()}"

    def getCSQ(self) -> dict[str, str]:
        if self.info.get("CSQ") is None:
            return dict()

        assert self.header.info.get("CSQ") != None

        # FIXME: Looks like a helper function
        header_string = self.header.info.get("CSQ")
        # FIXME: Check, does this always hold?
        assert header_string.description is not None
        # FIXME: More robust with regex
        header_fields = header_string.description.split("Format: ")[1].split("|")

        value_string = self.info["CSQ"][0]
        values = value_string.split("|")

        assert len(header_fields) == len(values), print(len(header_fields), len(values))

        csq_dict = dict()
        for i in range(len(header_fields)):
            header = header_fields[i]
            value = values[i]
            csq_dict[header] = value
        return csq_dict

    def __init__(
        self,
        contig: str,
        pos: int,
        ref: str | None,
        alt: tuple[str, ...] | None,
        rankScore: int | None,
        info: dict[str, tuple[str]],
        header: VariantHeader,
    ):
        self.contig = contig
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.score = rankScore
        self.info = info
        self.header = header


class Dataset:
    __fh: VariantFile
    _variantDict: dict[str, Variant]
    _filepath: str
    _scores: list[int]
    label: str
    variants: list[Variant]

    def __init__(self, label, filename):
        self.label = label
        self._filepath = filename
        self._scores = list()
        self.variants = list()
        self._variantDict = dict()

    def hasScores(self) -> bool:
        return len(self._scores) > 0

    def getScores(self) -> list[int]:
        return self._scores

    def getVariantByKey(self, key: str) -> Variant | None:
        return self._variantDict.get(key)

    def getScoreByKey(self, key: str) -> int | None:
        var = self._variantDict.get(key)
        if var is None:
            return None
        return var.score

    def getVariantKeys(self) -> set[str]:
        return set([var.getKey() for var in self.variants])

    def getTopScoredVariantKeys(self, top_n: int) -> set[str]:
        sorted_variants = sorted(
            self.variants,
            key=lambda var: var.score if var.score is not None else -1,
            reverse=True,
        )
        variant_keys = [var.getKey() for var in sorted_variants[0:top_n]]
        return set(variant_keys)

    def getAnnotations(self) -> list[str]:
        return [info[0] for info in self.__fh.header.info.items()]

    def parse(self, score_key: str | None = None, contigs=None) -> None:
        self.__fh = VariantFile(self._filepath)
        fh = self.__fh.fetch(contigs)
        has_rank_score = (
            score_key is not None and self.__fh.header.info.get(score_key) is not None
        )
        for record in fh:
            rank_score = None
            if score_key is not None and has_rank_score:
                rank_score_cell = record.info.get(score_key)
                rank_score = int(rank_score_cell[0].split(":")[-1])
                self._scores.append(rank_score)

            variant = Variant(
                record.contig,
                record.pos,
                record.ref,
                record.alts,
                rank_score,
                {item[0]: item[1] for item in record.info.items()},
                record.header,
            )
            self.variants.append(variant)
            self._variantDict[variant.getKey()] = variant

    def __str__(self):
        return f"{self.label}\t{len(self.variants)}\t{self._filepath}"
