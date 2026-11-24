# oamd-bio-test-data
This repository contains test data to be used for automated testing of Advance Molecular Detection Platform pipelines. 

> ⚠️ **Do not merge your test data to `master`! Each pipeline has a dedicated branch (and a special one for modules)**

## Introduction

ph-core's set up mirrors that of nf-core. ph-core is a collection of high quality Nextflow workflows, subworkflows, and modules related to genomic surveillance. This repository contains various files for CI and unit testing of ph-core pipelines and infrastructure.

The principle for ph-core test data is the same as nf-core test data in that the data should be as small as possible, as large as necessary. Please see the [guidelines](https://nf-co.re/docs/contributing/test_data_guidelines) for nf-core test datasets for more detailed information.

## Downloading test data

Due the large number of large files in this repository for each pipeline, we highly recommend cloning only the branches you would use.

```bash
git clone <url> --single-branch --branch <pipeline/modules/branch_name>
```

To subsequently clone other branches[^1]

```bash
git remote set-branches --add origin [remote-branch]
git fetch
```

## MSATree test data

This branch holds the inputs of the [MSATree](https://github.com/cdcent/oamd-bio-msatree) pipeline tests (`tests/*.nf.test` and the `test`, `test_dengue` and `test_full` profiles), which read them from `https://raw.githubusercontent.com/CDCgov/oamd-bio-test-data/refs/heads/msatree/`. Each consensus FASTA holds one record whose header is the sample name, as MSATree requires, except where the table says otherwise.

| Path | Content | Used by | Source |
| --- | --- | --- | --- |
| `samples/positive_control_1.fa`, `samples/positive_control_2.fa`, `samples/test_sample_3.fa`, `samples/test_sample_8.fa` | Measles consensus genomes. The two positive controls are the same sequence | `samplesheet_msatree.csv` (`test` profile) and the variants below | Added for the MEATree pipeline test in `ab270ae`; headers set to the sample names in `32693a0` |
| `samples/ivar_header.fa` | The `test_sample_8` genome with iVar's default consensus header (`>Consensus_test_sample_8_threshold_0.75_quality_20`) | `samplesheet_msatree_header_check.csv`, `samplesheet_msatree_too_few.csv` | `32693a0` |
| `samples/positive_control_1.no_final_newline.fa` | `positive_control_1.fa` without its final newline | `samplesheet_msatree_no_final_newline.csv` | Made from `positive_control_1.fa` with `head -c -1` |
| `samples/MMR*.consensus.fa`, `samples/MVs_*.consensus.fa`, `samples/ROM_129_IF_2_28_2024.consensus.fa` | 12 measles consensus genomes | `samplesheet_msatree_full.csv` (`test_full` profile) | `88d5c98` |
| `samples/dengue/D10_NOV2023.fa`, `D11_NOV2023.fa`, `D12_NOV2023.fa` | Dengue consensus genomes | `samplesheet_msatree_dengue.csv` (`test_dengue` profile). `D10_NOV2023` is also in `samplesheet_msatree_nextclade_unaligned.csv`, as a genome that Nextclade cannot align to the measles reference | The same sequences as `data/genomics/viral/dengue/NextcladeRunSerotypeBatch_input/` on the `modules` branch |
| `samples/dengue/sample_0001.fa` to `sample_0003.fa` | Dengue consensus genomes | `samplesheet_msatree_dengue.csv` | `67aec98` |
| `references/NC_001498_1.fasta` | Measles virus complete genome | `--genome_ref` for `--aligner nextclade` | NCBI RefSeq NC_001498.1 |
| `references/dengue_serotype_refs.fasta` | DENV1 to DENV4 complete genomes (NC_001477.1, NC_001474.2, NC_001475.2, NC_002640.1) | `--genome_ref` (`test_dengue` profile) | NCBI RefSeq |
| `references/n450_ref.fasta`, `references/mfncr_ref.fasta` | Measles N-450 (450 nt) and MF-NCR (1,018 nt) region references | `--n450_ref`, `--mfncr_ref` | `9d00ef4` |
| `dsid/fake_dsids_for_testing.fa` | Two made-up DSIDs, `abc1` and `xyz2`, holding the N-450 regions of `test_sample_3` and `test_sample_8` | `--n450_dsid_db` | Made for the tests in `287f11f` |
| `microreactshapes/metadata*.csv` | Collection date and place of the samples in the matching samplesheet | `--metadata` | Made for the tests |
| `microreactshapes/geolocation.csv` | Geolocation centroid lookup | `--geolocation` | Copy of `data/genomics/viral/measles/microreactshapes/geolocation.csv` on the `modules` branch (`e816abc`) |
| `samplesheet/*.csv` | Samplesheets that point at the files above | `--input` | Made for the tests |

## Public Domain Standard Notice
This repository constitutes a work of the United States Government and is not
subject to domestic copyright protection under 17 USC § 105. This repository is in
the public domain within the United States, and copyright and related rights in
the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this repository will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

## License Standard Notice
The repository utilizes code licensed under the terms of the Apache Software
License and therefore is licensed under ASL v2 or later.

This source code in this repository is free: you can redistribute it and/or modify it under
the terms of the Apache Software License version 2, or (at your option) any
later version.

This source code in this repository is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the Apache Software License for more details.

You should have received a copy of the Apache Software License along with this
program. If not, see http://www.apache.org/licenses/LICENSE-2.0.html

The source code forked from other open source projects will inherit its license.

## Privacy Standard Notice
This repository contains only non-sensitive, publicly available data and
information. All material and community participation is covered by the
[Disclaimer](DISCLAIMER.md)
and [Code of Conduct](code-of-conduct.md).
For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

## Contributing Standard Notice
Anyone is encouraged to contribute to the repository by [forking](https://help.github.com/articles/fork-a-repo)
and submitting a pull request. (If you are new to GitHub, you might start with a
[basic tutorial](https://help.github.com/articles/set-up-git).) By contributing
to this project, you grant a world-wide, royalty-free, perpetual, irrevocable,
non-exclusive, transferable license to all users under the terms of the
[Apache Software License v2](http://www.apache.org/licenses/LICENSE-2.0.html) or
later.

All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).

## Records Management Standard Notice
This repository is not a source of government records, but is a copy to increase
collaboration and collaborative potential. All government records will be
published through the [CDC web site](http://www.cdc.gov).

## Additional Standard Notices
Please refer to [CDC's Template Repository](https://github.com/CDCgov/template) for more information about [contributing to this repository](https://github.com/CDCgov/template/blob/main/CONTRIBUTING.md), [public domain notices and disclaimers](https://github.com/CDCgov/template/blob/main/DISCLAIMER.md), and [code of conduct](https://github.com/CDCgov/template/blob/main/code-of-conduct.md).