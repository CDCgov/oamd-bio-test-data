# Synthetic TALOS test samples

Paired-end samples with known content, so the TALOS pipeline tests exercise real findings. All
reads are simulated or come from this branch's public test reads; there is no patient data.

| Sample | Content | Expected TALOS report |
|---|---|---|
| `synthetic_positive_1` | Influenza B virus 30x, Human Metapneumovirus 30x, Coronavirus OC43 20x | 3 findings |
| `synthetic_positive_2` | Influenza A virus A/H1-2009 25x, Adenovirus C 15x | 2 findings |
| `synthetic_low` | Human Rhinovirus Enterovirus 8 pairs, Bordetella pertussis 500 pairs | none pass the detection filter |
| `synthetic_negative` | background only | nothing |

Every sample also holds 20,000 background pairs. Fold coverage is per panel record; `<sample>.truth.tsv` lists the
records, pairs and fold coverage drawn for each organism.

**Made with** `simulate_talos_test_reads.py` (in this folder), seed 20261120:

    simulate_talos_test_reads.py --panel references/respiratory_panel_dx.fasta \
        --mapping references/talos_respiratory_panel_dx.mapping \
        --background_r1 bg_clean_R1.fastq.gz --background_r2 bg_clean_R2.fastq.gz \
        --spec samples.tsv --outdir samples/synthetic

- Reads: 150 bp, fragments ~N(300, 30), 0.2 % substitutions, quality 40, drawn from the panel records of each
  organism in `samples.tsv`.
- Background (`bg_clean`): the pairs of `samples/negative_control_1_subset_R{1,2}.fastq.gz` with no
  `minimap2 -x sr` hit on `references/respiratory_panel_dx.sr.mmi` (49,943 pairs). Reads are taken from the
  original FASTQ, so their headers keep the comment field.

## Test Kraken2 database

`references/talos_test_kraken2_db.tar.gz` is built from `references/test_panel_sequences_tagged.fasta`: the 57
records of `respiratory_panel_dx.fasta`, each tagged with its NCBI taxid, plus 10 Mbp of human chromosome 22
(taxid 9606). Kraken2 2.1.6, NCBI taxonomy (`taxdump.tar.gz`, md5 `cb98f5505aa40d69062bc03da7144877`), default
k-mer settings:

    kraken2-build --add-to-library references/test_panel_sequences_tagged.fasta --db talos_test_kraken2_db_minimal
    kraken2-build --build --db talos_test_kraken2_db_minimal
    tar -czf talos_test_kraken2_db.tar.gz talos_test_kraken2_db_minimal/{hash,opts,taxo}.k2d

Multi-threaded builds are not byte-identical, but they classify the test samples the same way.
