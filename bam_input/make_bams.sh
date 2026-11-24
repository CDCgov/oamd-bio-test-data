#!/usr/bin/env bash
# Builds the qqq BAM-input fixtures from nf-core test reads. Runs inside a minimap2+samtools image.
set -eu
cd /out
gzip -cd /src/test_1.fastq.gz  | head -n 8000 | gzip -n > pe_1.fastq.gz
gzip -cd /src/test_2.fastq.gz  | head -n 8000 | gzip -n > pe_2.fastq.gz
# drop the /1 suffix: real single-end reads carry none, and samtools import reads it as READ1
gzip -cd /src/test2_1.fastq.gz | head -n 8000 | awk 'NR%4==1 {sub(/\/1$/, "")} {print}' | gzip -n > se.fastq.gz
gzip -cd /src/sample1_R1.fastq.gz | head -n 8000 | gzip -n > long.fastq.gz
# unaligned, name-grouped (as an instrument writes it)
samtools import -1 pe_1.fastq.gz -2 pe_2.fastq.gz -o ubam_pe.bam
samtools import -0 se.fastq.gz -o ubam_se.bam
samtools import -0 long.fastq.gz -o ubam_long_nanopore.bam
# the same library aligned and coordinate-sorted, with secondary and supplementary records
minimap2 -ax sr -N 5 --secondary=yes -t 4 /src/chr21.fasta pe_1.fastq.gz pe_2.fastq.gz 2>/dev/null \
  | samtools sort -o aligned_primary_secondary.bam -
# minimap2 writes no supplementary records for these short reads, so add one for each of the
# first 50 mapped primary records, shaped like a real one: flag + 0x800, the first 50 bases
# kept and the rest hard-clipped. Should one leak into the FASTQ, samtools fastq pairs it in
# place of its primary, so the read comes out 50 bases long and the comparison fails.
samtools view -h aligned_primary_secondary.bam \
  | awk 'BEGIN{OFS="\t"} /^@/ {print; next} {print}
         (int($2/256)%2 == 0 && int($2/4)%2 == 0 && length($10) > 60 && ++n <= 50) {
           L = length($10); $2 = $2 + 2048; $6 = "50M" (L - 50) "H"
           $10 = substr($10, 1, 50); $11 = substr($11, 1, 50); print }' \
  | samtools sort -o aligned_pe.sorted.bam -
rm aligned_primary_secondary.bam
# paired uBAM in which the first 100 pairs lost their read 2 (100 orphan read-1 records)
samtools view -h ubam_pe.bam | awk 'BEGIN{OFS="\t"} /^@/ {print; next} { if (int($2/128)%2 == 1 && ++n <= 100) next; print }' \
  | samtools view -b -o ubam_pe_orphans.bam -
for b in *.bam; do
  echo "$b: total=$(samtools view -c $b) primary=$(samtools view -c -F 0x900 $b) secondary=$(samtools view -c -f 0x100 $b) supplementary=$(samtools view -c -f 0x800 $b) paired=$(samtools view -c -f 1 $b) unmapped=$(samtools view -c -f 4 $b) SO=$(samtools view -H $b | grep -o 'SO:[a-z]*' || echo none)"
done
samtools --version | head -1; minimap2 --version
ls -la
