# Modules Test Data

This branch of the `oamd-bio-test-data` repository contains all data used for the individual module tests.
There are three main directories: `generic`, `genomics` and `delete_me`. The first contains generic files, the second contains all datasets for genomics tools while the latter contains temporary datasets that will be deleted as better data gets available.

## Adding New Data

If you cannot find suitable test data on this repository, please contact us on the [nf-core Slack `#modules` channel](https://nfcore.slack.com/channels/modules) (you can join with [this invite](https://nf-co.re/join/slack)). The goal is to create a suitable, small test dataset that should be usable with the available test data and if possible be generated with modules available from `nf-core/modules`. If creating that test data is difficult but you want to add the module first, it is also possible to add a small subset to the `delete_me` folder to get your module tests running, and then add proper test data afterwards. This should be discussed on slack. In order to add test data. For a short description of the workflow for adding new data, have a look at [here](docs/ADD_NEW_DATA.md).

### delete_me

The `delete_me` folder does not adhere to a defined structure as data in this folder should be delete as fast as possible, whenever a more suitable dataset is found that can be added to any other folder.

### generic

The `generic` folder contains generic files that currently cannot be associated to a genomics category. They are organised by their respective file extension. Also, it contains depreciated files which will be removed in the future and exchanged by files in `genomics`.

### genomics

The genomics folder contains subfolders for all organisms for which test data is available. At the moment, there are these organisms available in various places:

- influenza 

All folders are structured in a similar way, with any genome-specific files in `genome` (e.g. fasta, gtf, ...) and technology specific raw-data files in the `10xgenomics`, `illumina`, `nanopore`, `pacbio`, `hic` and `cooler` subfolders whenever available.
`Genomics` contains all typical data required for genomics modules, such as fasta, fastq and bam files. Every folder in `genomics` corresponds to a single organism. For every data file, a short description about how this file was generated is available either in this description or in the respective subfolder.

## Data Description

### genomics
- influenza
  - genome 
    - fa 
- rsv_a/rsv_b
  - genome 
    - fa 
- sars-cov-2
  - genome 
    - fa 
- viral/measles: fixtures of the [MSATree](https://github.com/cdcent/oamd-bio-msatree) local module tests
  - `msatree_hashing/test_n450.fasta`: one 450-nt N-450 region (`Consensu_test_1:1232-1682`, in the `bedtools getfasta` name format); `msatree_hashing/n450_ref.fasta`: the N-450 region reference (450 nt). Used by `REGION_HASHING`
  - `prepare_data/test.msa.fasta`, `prepare_data/test.nwk`: an alignment of a reference (`D8_9171_REF`) and four measles samples, and a tree of the same five sequences; `prepare_data/test_metadata.csv`: test metadata for the four samples. Used by `PREPARE_DATA`
  - `bundle_viewer/test.data.json`: viewer data in the `PREPARE_DATA` output format; `bundle_viewer/viewer.html`: a viewer template with the `EMBEDDED_DATA = null` placeholder. Used by `BUNDLE_VIEWER`
  - `microreactshapes/metadata.csv`, `microreactshapes/samplesheet.csv`: test metadata and samplesheet for four samples; `microreactshapes/geolocation.csv`: geolocation centroid lookup, also copied to the `msatree` branch. Used by `MICROREACTSHAPES`
- viral/dengue
  - `NextcladeRunSerotypeBatch_input/D10_NOV2023.consensus.fa` to `D12_NOV2023.consensus.fa`: Dengue consensus genomes. The same sequences are the `D10_NOV2023` to `D12_NOV2023` samples of the MSATree Dengue pipeline test on the `msatree` branch
        
### generic

### Uncategorized

Followed guidance [here](https://github.com/nf-core/test-datasets/blob/modules/README.md)