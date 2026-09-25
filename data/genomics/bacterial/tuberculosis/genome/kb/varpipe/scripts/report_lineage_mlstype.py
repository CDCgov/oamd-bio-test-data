#!/usr/bin/env python3

import json
import sys
import re
import csv


def parse_lineage(lineage_file, sample_id):
    with open(lineage_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 3 and parts[0] == sample_id:
                lineage = parts[1]
                lineage_name = parts[2]
                if lineage_name == "mixed_lineage(s)":
                    return "NoResult"
                else:
                    return "{} (L{})".format(lineage_name, lineage)


def parse_mlstype(outputs_json, sample_id):
    with open(outputs_json, "r") as f:
        data = json.load(f)

    # Extract directly from the strain_names dictionary
    strain_names = data.get("result", {}).get("strain_names", {})
    # Return the strain name directly without formatting
    return strain_names.get(sample_id, "")


def main():
    sample_id = sys.argv[1]
    outputs_json = sys.argv[2]
    lineage_file = sys.argv[3]
    output_csv = sys.argv[4]

    lineage = parse_lineage(lineage_file, sample_id)

    mlstype = parse_mlstype(outputs_json, sample_id)

    with open(output_csv, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["sample_id", "lineage", "wg_mlstype"])
        writer.writerow([sample_id, lineage, mlstype])


if __name__ == "__main__":
    main()
