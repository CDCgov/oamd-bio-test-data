#!/usr/bin/env python3
"""Simulate TALOS test samples with known content: paired-end reads from chosen test-panel organisms,
mixed into background reads that do not map to the panel.

usage: simulate_talos_test_reads.py --panel respiratory_panel_dx.fasta --mapping talos_respiratory_panel_dx.mapping
           --background_r1 bg_R1.fastq.gz --background_r2 bg_R2.fastq.gz --spec samples.tsv --outdir samples/synthetic

samples.tsv (tab-separated, header): sample, organism, depth, pairs
  one row per organism in a sample: `organism` is the mapping's Organism; give either `depth` (fold
  coverage of each of the organism's records) or `pairs` (read pairs spread over its records by length).
  A row with organism `-` and `pairs` N adds N background pairs; a sample with no other rows is a negative.

Reads: 150 bp, fragment length ~N(300, 30), 0.2% substitutions, Phred 40 ('I'), forward/reverse strand
at random, read names `<sample>:<organism record>:<n>` (background keeps its own names). Deterministic for
a given --seed. Output: <outdir>/<sample>_R1.fastq.gz, _R2.fastq.gz and <outdir>/<sample>.truth.tsv.
"""
import argparse
import csv
import gzip
import random

READ_LEN, FRAG_MEAN, FRAG_SD, ERR = 150, 300, 30, 0.002
COMP = str.maketrans("ACGTNacgtn", "TGCANtgcan")


def revcomp(s):
    return s.translate(COMP)[::-1]


def read_fasta(path):
    seqs, name, parts = {}, None, []
    for line in open(path):
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(parts).upper()
            name, parts = line[1:].split()[0], []
        else:
            parts.append(line.strip())
    if name:
        seqs[name] = "".join(parts).upper()
    return seqs


def mutate(seq, rng):
    out = list(seq)
    for i in range(len(out)):
        if rng.random() < ERR:
            out[i] = rng.choice([b for b in "ACGT" if b != out[i]])
    return "".join(out)


def pairs_from(record, seq, n, rng, sample):
    for k in range(n):
        frag = max(READ_LEN, int(rng.gauss(FRAG_MEAN, FRAG_SD)))
        if len(seq) < frag:
            frag = len(seq)
        start = rng.randint(0, len(seq) - frag)
        f = seq[start:start + frag]
        if rng.random() < 0.5:
            f = revcomp(f)
        r1, r2 = f[:READ_LEN], revcomp(f)[:READ_LEN]
        name = f"{sample}:{record}:{k}"
        yield (name, mutate(r1, rng)), (name, mutate(r2, rng))


def fastq_pairs(r1, r2):
    with gzip.open(r1, "rt") as a, gzip.open(r2, "rt") as b:
        while True:
            h1, s1, _, q1 = (a.readline().rstrip() for _ in range(4))
            h2, s2, _, q2 = (b.readline().rstrip() for _ in range(4))
            if not h1:
                return
            yield (h1, s1, q1), (h2, s2, q2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    for k in ("panel", "mapping", "background_r1", "background_r2", "spec", "outdir"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--seed", type=int, default=20261120)
    a = ap.parse_args()

    panel = read_fasta(a.panel)
    records = {}
    for row in csv.DictReader(open(a.mapping), delimiter="\t"):
        records.setdefault(row["Organism"], []).append(row["Contig"])
    spec = {}
    for row in csv.DictReader(open(a.spec), delimiter="\t"):
        spec.setdefault(row["sample"], []).append(row)
    background = list(fastq_pairs(a.background_r1, a.background_r2))

    import os
    os.makedirs(a.outdir, exist_ok=True)
    for sample, rows in spec.items():
        rng = random.Random(f"{a.seed}:{sample}")
        reads, truth = [], []
        for row in rows:
            if row["organism"] == "-":
                n = int(row["pairs"])
                for (h1, s1, q1), (h2, s2, q2) in rng.sample(background, n):
                    reads.append(((h1, s1, q1), (h2, s2, q2)))
                truth.append((sample, "background", "", n, ""))
                continue
            recs = records[row["organism"]]
            total = sum(len(panel[r]) for r in recs)
            for r in recs:
                seq = panel[r]
                if row.get("depth"):
                    n = max(1, round(float(row["depth"]) * len(seq) / (2 * READ_LEN)))
                else:
                    n = max(0, round(int(row["pairs"]) * len(seq) / total))
                for p1, p2 in pairs_from(r, seq, n, rng, sample):
                    reads.append(((f"@{p1[0]}/1", p1[1], "I" * len(p1[1])), (f"@{p2[0]}/2", p2[1], "I" * len(p2[1]))))
                truth.append((sample, row["organism"], r, n, round(2 * READ_LEN * n / len(seq), 2)))
        rng.shuffle(reads)
        with gzip.open(f"{a.outdir}/{sample}_R1.fastq.gz", "wt", compresslevel=9) as o1, \
             gzip.open(f"{a.outdir}/{sample}_R2.fastq.gz", "wt", compresslevel=9) as o2:
            for (h1, s1, q1), (h2, s2, q2) in reads:
                o1.write(f"{h1}\n{s1}\n+\n{q1}\n")
                o2.write(f"{h2}\n{s2}\n+\n{q2}\n")
        with open(f"{a.outdir}/{sample}.truth.tsv", "w") as t:
            t.write("sample\torganism\trecord\tpairs\tfold_coverage\n")
            for r in truth:
                t.write("\t".join(map(str, r)) + "\n")
        print(f"{sample}: {len(reads)} pairs")


if __name__ == "__main__":
    main()
