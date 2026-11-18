# NextcladeDatasetgetSerotype_input — no file test data

`NEXTCLADE_DATASETGET_SEROTYPE` takes only string values:

```
input:
tuple val(serotype), val(dataset), val(tag)
```

e.g. `serotype = 'DENV1'`, `dataset = 'community/v-gen-lab/dengue/denv1'`,
`tag = '2026-04-14--11-55-23Z'`. There are no files to deposit — the module runs
`nextclade dataset get`, which fetches the dataset over the network at test time.

The `tests/main.nf.test` for this module supplies those strings directly and asserts the
downloaded dataset directory exists (e.g. `pathogen.json` / `tree.json` present). This folder
is kept only so every new module has a matching `*_input/` entry.
