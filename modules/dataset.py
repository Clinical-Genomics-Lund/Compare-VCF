from pysam import VariantFile


class Dataset:
    _hasScore: bool = False
    _label: str
    _filepath: str
    _variants: set[str]

    def __init__(self, label, filename):
        self._label = label
        self._filepath = filename
        self._variants = set()

    def parse(self, contigs=None):
        print(f">>> file path {self._filepath}")
        vcf_in = VariantFile(self._filepath)
        fh = vcf_in.fetch(contigs)
        for record in fh:
            pos_name = f"{record.contig}:{record.pos}"
            self._variants.add(pos_name)
        print(f"Number variants: {len(self._variants)}")

    def __str__(self):
        return f"{self._label}\t{len(self._variants)}\t{self._filepath}"
