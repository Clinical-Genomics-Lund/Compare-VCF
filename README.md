The purpose of this tool is to provide convenient utilities to evaluate calling and annotation differences between VCF files.

The common use case would be that different technical approaches have been used for the same biological samples, and that the impact from these choices need to be understood.

### Install dependencies

This is recommended to do within a `venv` environment ([link](https://docs.python.org/3/library/venv.html))

```
pip install -r requirements.txt
```

### Usage

Inputs can be gzipped.

The functionality is organized into sub commands. Currently the two commands are `overview` and `rankmodels`.

```
python compare_vcf.py overview \
    --inputs run1.vcf.gz run2.vcf.gz run3.vcf.gz \
    --labels first second third \
    --outdir testout \
    --contig chr20    # If you want to quickly run a subset of the data
```

For comparing rank model and rank model scores among variants.

```
python compare_vcf.py rankmodels \
    --inputs run1.vcf.gz run2.vcf.gz run3.vcf.gz \
    --labels first second third \
    --outdir testout \
    --topn 200 \
    --rankmodels "" run2_model.ini run3_model.ini \ # Optional, "" for missing if some rank models are present
    --contig chr20
```

### Subset of outputs

FIXME: Update to show latest outputs for each of the sub commands.

Number called variants among the different vcf-files.

![Total counts](docs/1_total_counts.png)

Overlaps among the called variants. More info on the upset chart can be found [here](https://en.wikipedia.org/wiki/UpSet_Plot)

![Overlaps among counts](docs/2_overlaps.png)

If a scoring metric is provided, histograms of the scores are generated for each dataset.

![Score histograms](docs/3_score_histograms.png)

If a scoring metric is provided, heatmaps comparing the number of features with shared scorings are also generated.

![Score heatmaps](docs/4_score_heatmap.png)

Score table. This will be extended.

![Score table](docs/5_score_table.PNG)

### Planned extensions

* More detailed annotation information in the output table.
* Use the GIAB as a reference base line.

