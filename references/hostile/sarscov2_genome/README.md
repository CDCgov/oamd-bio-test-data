# Pipeline test data

A hostile/hostess index of the SARS-CoV-2 genome that `-profile test` uses as its host (nf-core
test-datasets `genomics/sarscov2/genome/genome.fasta`, md5 `6e9fe4042a72f2345f644f239272b7e6`),
laid out the way hostile publishes its indexes: `--hostile_db` is this directory and
`--hostile_index` is `sarscov2_genome`. Prebuilt because the pipeline never builds an index, in
tests or in production. Two builds of each were byte-identical.

| file | aligner | built in |
|---|---|---|
| `sarscov2_genome.{1,2,3,4,rev.1,rev.2}.bt2` | bowtie2 (short reads) | AMDP `oamd-bio-bowtie2:2.5.4` |
| `sarscov2_genome.mmi` | minimap2 (long reads), `map-ont` preset | AMDP `oamd-bio-hostile:2.0.2` (minimap2 2.26) |

```bash
bowtie2-build --threads 1 --seed 0 genome.fasta sarscov2_genome
minimap2 -x map-ont -d sarscov2_genome.mmi genome.fasta   # the command hostile runs to build its own .mmi
```
