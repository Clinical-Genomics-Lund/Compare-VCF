The purpose of this tool is to provide convenient utilities to evaluate calling and annotation differences between VCF files.

The common use case would be that different technical approaches have been used for the same biological samples, and that the impact from these choices need to be understood.

### Install dependencies

```
pip install -r requirements.txt
```

### Usage

Inputs can be gzipped.

```
python evaluate.py \
    --inputs run1.vcf.gz run2.vcf.gz run3.vcf.gz \
    --labels first second third \
    --outdir testout
```

#### Useful settings

* `--contig "chr1"` Limit analysis to one contig.

### TODO

Task-list:

* Table comparison of top-list
* Correlation calculation of "top-X" features
* RTG convenience wrapper (for GIAB samples only)

For now, `rtg` has been used as below.

```
/src/bnf/rtg-tools-3.12.1/rtg vcfeval \
    --baseline data/231004_giab_nist/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz \
    -c data/231006_nfcore_filtered_annotated/testout.vcf.gz \
    --output testrun -t data/GRCh38.sdf
```

