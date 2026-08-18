# oamd-bio-test-data: `wepp`

Test data for [`cdcent/oamd-bio-wepp`](https://github.com/cdcent/oamd-bio-wepp), the
AMD Platform Nextflow wrapper around
[WEPP](https://github.com/TurakhiaLab/WEPP).

> ⚠️ **Do not merge this branch to `master`.** Each pipeline has its own branch.

## Contents

| Path | Description |
| --- | --- |
| `samples/RSVA_sub_R{1,2}.fastq.gz` | ENA run [ERR14763711](https://www.ebi.ac.uk/ena/browser/view/ERR14763711), an RSV-A wastewater sample, subsampled to the first 100,000 read pairs |
| `testdata/rsvA.latest.pb.gz` | RSV-A mutation-annotated tree, from the [UShER hub](https://hgdownload.gi.ucsc.edu/hubs/GCF/002/815/475/GCF_002815475.1/UShER_RSV-A/) |
| `testdata/GCF_002815475.1_ASM281547v1_genomic.fna` | RSV-A reference (NC_038235.1), uncompressed as WEPP requires |
| `samplesheet/samplesheet.csv` | Points at the subsampled reads — used by `-profile test` |
| `samplesheet/samplesheet_full.csv` | Points at the full ENA run — used by `-profile test_full` |

All of it is public data. Nothing here is sensitive.

## Provenance

The dataset mirrors WEPP's own RSV-A quickstart. The reads were subsampled with
`zcat … | head -n 400000` on each mate, which keeps the pair ordering intact, and
recompressed with `gzip -9`, bringing 286 MB down to 11 MB.

The subsample is small but not vacuous — it still exercises the whole pipeline and
produces a real answer rather than an empty one:

```
5 lineages    A.D 0.573, A.D.1.6 0.259, A.D.1 0.102, A.D.3 0.058, A 0.008
10 haplotypes
11 unaccounted alleles
```

Note the lineage mix differs from the full run (which gives A.D.3 0.444 / A.D 0.297 /
A.D.1 0.259) — that is expected from reading only the head of the file, and is why
`test_full` exists. Use `test` to check that the pipeline runs, not to check numbers.

RSV-A carries a single lineage naming system, so the pipeline must be run against
this data with `--wepp_clade_list annotation_1 --wepp_clade_idx 0`. Both test
profiles set that already.

## Refreshing the MAT

`rsvA.latest.pb.gz` is a snapshot. UCSC now publishes only a rolling `latest` and no
longer keeps dated subdirectories, so the tree here is pinned by being committed. If
it is refreshed, the expected lineage output above will change.
