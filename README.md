Overview information should come here

Analysis scripts, should probably be organized in the `scripts` folder.

First prepare chromosome-based names with `tbi` index.

If multiple annotations, it can be run using the `remove_duplicate_info.py` script (which simply seems to put INFO in a dictionary, resulting in the trimming of that field).

For now, `rtg` has been used as below.

```
/src/bnf/rtg-tools-3.12.1/rtg vcfeval \
    --baseline data/231004_giab_nist/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz \
    -c data/231006_nfcore_filtered_annotated/testout.vcf.gz \
    --output testrun -t data/GRCh38.sdf
```

Things to fix:

* X, Y and MT chromosomes?
