#!/usr/bin/env python3

import argparse
import csv
import os
import gzip
from pathlib import Path

def transpose_file(input_file, output_file):
    """Transpose gzipped CSV file."""
    with gzip.open(input_file, 'rt') as f:
        data = [line.strip().split(',') for line in f]
        transposed = []
        for i in range(len(data[0])):
            row = []
            for j in range(len(data)):
                cell = data[j][i].strip()
                row.append(cell)
            transposed.append(' '.join(row))

    with open(output_file, 'w') as f:
        f.write('\n'.join(transposed))

def process_input_files(input_dir, output_dir):
    """Process and transpose each input file."""
    os.makedirs(output_dir, exist_ok=True)

    for input_file in Path(input_dir).glob('*_calls_core_standard.csv.gz'):
        sample_id = input_file.stem.replace('_calls_core_standard.csv', '')
        output_file = Path(output_dir) / f"{sample_id}_calls_core_standard_transpose.txt"

        print(f"Processing {sample_id}...")
        transpose_file(input_file, output_file)

def combine_samples(input_dir, header_file, outfile):
    """Combine transposed files into single CSV."""
    with open(header_file) as handle:
        columns = dict((line.strip(), "") for line in handle if line.strip())

    sample_files = [
        input_dir / filename
        for filename in os.listdir(input_dir)
        if filename.endswith("_transpose.txt")
    ]

    with open(outfile, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns.keys(), lineterminator="\n")
        writer.writeheader()
        for sample_file in sample_files:
            with open(sample_file) as handle:
                writer.writerow(
                    columns.copy() | dict(line.strip().split() for line in handle)
                )

def main():
    parser = argparse.ArgumentParser(
        description="Process core calls files for wgMLSTyping"
    )
    parser.add_argument(
        "--input_dir",
        required=True,
        help="Input directory containing calls_core_standard.csv.gz files"
    )
    parser.add_argument(
        "--temp_dir",
        required=True,
        help="Temporary directory for transposed files"
    )
    parser.add_argument(
        "--outfile",
        required=True,
        help="Output CSV file path for wgMLSType workflow"
    )
    parser.add_argument(
        "--header_file",
        required=True,
        help="Header file path for wgMLSType workflow"
    )

    args = parser.parse_args()

    process_input_files(args.input_dir, args.temp_dir)

    combine_samples(Path(args.temp_dir), Path(args.header_file), Path(args.outfile))
    print(f"Combined calls written to {args.outfile}")

if __name__ == "__main__":
    main()
