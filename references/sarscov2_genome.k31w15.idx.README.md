# Pipeline test data

- `sarscov2_genome.k31w15.idx`: a deacon minimizer index (k = 31, w = 15, deacon's defaults) of
  the SARS-CoV-2 genome that `-profile test` uses as its host (nf-core test-datasets
  `genomics/sarscov2/genome/genome.fasta`, md5 `6e9fe4042a72f2345f644f239272b7e6`), for the
  default `--dehoster deacon`. Prebuilt because the pipeline never builds an index, in tests or
  in production. Built in the AMDP `oamd-bio-deacon:0.20.0` image; two builds were
  byte-identical:

  ```bash
  deacon index build --threads 1 --output sarscov2_genome.k31w15.idx genome.fasta
  ```
