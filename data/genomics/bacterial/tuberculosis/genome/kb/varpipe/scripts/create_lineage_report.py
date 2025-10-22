#!/usr/bin/env python3

import sys
import os


def create_lineage_report(inputFile, outputFile):
    with open(inputFile, "r") as f:
        lines = f.readlines()

    lineage = ""
    lineage_name = ""
    for line in lines:
        line = line.strip()
        if "no precise lineage inferred" in line:
            lineage = "mixed lineage(s)"
            lineage_name = "mixed lineage(s)"
        elif "Lineage:" in line:
            parts = line.split(":")
            if len(parts) >= 3:
                lineage = parts[1].strip().split()[0]
                lineage_name = parts[2].strip()
            elif len(parts) == 2:
                lineage_parts = parts[1].strip().split(None, 1)
                if len(lineage_parts) >= 2:
                    lineage = lineage_parts[0]
                    lineage_name = lineage_parts[1]
            else:
                lineage = lineage_parts[0]

    sample = os.path.basename(inputFile).split("_")[0]

    with open(outputFile, "w") as f:
        f.write("Sample ID\tLineage\tLineage Name\n")
        f.write("{0}\t{1}\t{2}\n".format(sample, lineage, lineage_name))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python create_lineage_report.py inputFile outputFile. inputFile should be Lineage.txt file."
        )
        sys.exit(1)

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    create_lineage_report(inputFile, outputFile)
