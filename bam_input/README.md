# BAM input fixtures

Test data for qqq's BAM input (the samplesheet's `bam` column, AMD-35820). qqq converts a BAM
to FASTQ before any other step, and works out from the records whether it is paired. Each BAM
below has a FASTQ beside it holding the reads it was built from, so a test can check the
conversion gives back exactly those reads, with their pairing.

| file | what it is | records | what it tests |
| --- | --- | --- | --- |
| `ubam_pe.bam` | unaligned, paired, name-grouped (`samtools import`) | 4,000 (2,000 pairs) | the usual uBAM |
| `aligned_pe.sorted.bam` | the **same library**, aligned to chr21 with minimap2 and coordinate-sorted | 5,014: 4,000 primary, 964 secondary, 50 supplementary, 52 unmapped | mates scattered by sorting; secondary and supplementary records must be dropped |
| `ubam_se.bam` | unaligned, single-end (no 0x1 flag) | 2,000 | single-end layout |
| `ubam_pe_orphans.bam` | `ubam_pe.bam` with read 2 removed from its first 100 pairs | 3,900: 1,900 pairs and 100 orphan read 1s | orphans |
| `ubam_long_nanopore.bam` | unaligned, single-end, the reads qqq's `-profile test` uses for its nanopore sample | 2,000 | long-read BAM |
| `source_pe_{1,2}.fastq.gz` | the reads `ubam_pe.bam`, `aligned_pe.sorted.bam` and `ubam_pe_orphans.bam` were built from | 2,000 pairs | |
| `source_se.fastq.gz` | the reads of `ubam_se.bam` | 2,000 | |
| `source_long.fastq.gz` | the reads of `ubam_long_nanopore.bam` | 2,000 | |

The 50 supplementary records are synthetic. minimap2 writes none for these short reads, so
one was added for each of the first 50 mapped primary records, shaped like a real one: 0x800
added to the flag, the first 50 bases kept and the rest hard-clipped. A leaked supplementary
or secondary record does not add a read: `samtools fastq` pairs it in place of its primary,
so the read comes out altered (50 bases, or the secondary's `*` sequence) and a comparison
against the source FASTQ catches it. Checked with samtools 1.22.1: `-F 0x900` returns the
source reads exactly, while `-F 0x100`, `-F 0x800` and `-F 0` each change them.

## Source

All reads come from nf-core/test-datasets, branch `modules`, and are the first 2,000 reads
or pairs of each file:

- paired: `genomics/homo_sapiens/illumina/fastq/test_{1,2}.fastq.gz`
- single-end: `genomics/homo_sapiens/illumina/fastq/test2_1.fastq.gz`, with the `/1` suffix
  removed from read names. `samtools import` takes that suffix to mean READ1 and would set
  the paired flags.
- long-read: `5f09ab078a7459db38c1ec86712a98d369cf7863/illumina/amplicon/sample1_R1.fastq.gz`
- reference for the aligned BAM: `genomics/homo_sapiens/genome/chr21/sequence/genome.fasta`

## Rebuilding

`make_bams.sh` builds every file. It expects those inputs in `/src`, named `test_1.fastq.gz`,
`test_2.fastq.gz`, `test2_1.fastq.gz`, `sample1_R1.fastq.gz` and `chr21.fasta`, and writes
to `/out`. It was run in `community.wave.seqera.io/library/minimap2_samtools:b09096fc890429ce`
(samtools 1.23.1, minimap2 2.30-r1287):

```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD/src:/src:ro" -v "$PWD/out:/out" \
  -v "$PWD/make_bams.sh:/make_bams.sh:ro" \
  community.wave.seqera.io/library/minimap2_samtools:b09096fc890429ce bash /make_bams.sh
```

The `source_*` files here are `make_bams.sh`'s `pe_1`, `pe_2`, `se` and `long` outputs,
renamed.
