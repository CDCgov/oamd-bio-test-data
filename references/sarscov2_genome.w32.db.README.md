# Pipeline test data

- `sarscov2_genome.w32.db`: a STAT k-mer database (k = 32, window 32) of the SARS-CoV-2 genome
  that `-profile test` uses as its host (`--host_fasta`, nf-core test-datasets
  `genomics/sarscov2/genome/genome.fasta`), for the `--dehoster sra_scrubber` test. Built with
  amd-ph-core `srahumanscrubber/builddb` (no protected sequences) in the AMDP
  `oamd-bio-sra-human-scrubber:2.2.1` image:

  ```bash
  printf '%s\t%s\n' "$(stat -c %s genome.fasta)" "$PWD/genome.fasta" > host.list
  build_index_of_each_file host.list 32 32 .w32.db
  mv genome.fasta.w32.db sarscov2_genome.w32.db
  ```
