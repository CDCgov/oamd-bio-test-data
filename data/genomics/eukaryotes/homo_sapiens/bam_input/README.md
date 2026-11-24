# BAM input fixtures

Test data for amd-ph-core `samtools/collatefastq`. These are the same files as `bam_input/` on
this repository's `qqq-1.0.0` branch, whose README and `make_bams.sh` describe in full how they
were built.

| file | what it is | records |
| --- | --- | --- |
| `ubam_pe.bam` | unaligned, paired, name-grouped | 4,000 (2,000 pairs) |
| `aligned_pe.sorted.bam` | the same library aligned to chr21 with minimap2, coordinate-sorted | 5,014: 4,000 primary, 964 secondary, 50 supplementary |
| `ubam_pe_orphans.bam` | `ubam_pe.bam` with read 2 removed from its first 100 pairs | 3,900: 1,900 pairs and 100 orphan read 1s |

The reads are the first 2,000 pairs of nf-core/test-datasets (`modules` branch)
`genomics/homo_sapiens/illumina/fastq/test_{1,2}.fastq.gz`. The 50 supplementary records are
synthetic, shaped like real ones: 0x800 added to the flag, the first 50 bases kept and the rest
hard-clipped. A leaked secondary or supplementary record does not add a read, because
`samtools fastq` pairs it in place of its primary, so a test has to compare the converted reads
of `aligned_pe.sorted.bam` with those of `ubam_pe.bam`, not just count them.
