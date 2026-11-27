# Prebuilt host indexes of the human test genome (40 kb of chr22)

Built once from nf-core/test-datasets `modules/data/genomics/homo_sapiens/genome/genome.fasta` (md5 `f315020d899597c1b57e5fe9f60f4c3e`), so tests use a
prebuilt index the way production runs do and never build one at run time. Each build was run
twice and gave byte-identical files.

| file | tool | built with |
|---|---|---|
| `deacon/genome.k31w15.idx` | deacon (minimizer index, k = 31, w = 15) | AMDP `oamd-bio-deacon:0.20.0` |
| `bowtie2/genome.{1,2,3,4,rev.1,rev.2}.bt2` | bowtie2 index, name `genome` (hostile, hostess) | AMDP `oamd-bio-bowtie2:2.5.4` |
| `minimap2/genome.mmi` | minimap2 index, `map-ont` preset (hostile, hostess) | AMDP `oamd-bio-hostile:2.0.2` (minimap2 2.26) |

```bash
deacon index build --threads 1 --output genome.k31w15.idx genome.fasta
bowtie2-build --threads 1 --seed 0 genome.fasta genome
minimap2 -x map-ont -d genome.mmi genome.fasta   # the command hostile runs to build its own .mmi
```

The bowtie2 files are what a hostile/hostess index directory holds; hostile finds them by the
index name (`genome`). Pass the files themselves, or a directory holding them.
