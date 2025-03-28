#!/usr/bin/env python3

import gzip
import os
import sys
import glob
import re

def read_fastq_headers(file_path, num_reads=1000):
    """Read headers from FASTQ file."""
    headers = []
    with gzip.open(file_path, 'rt') if file_path.endswith('.gz') else open(file_path, 'r') as f:
        line_num = 0
        for line in f:
            line_num += 1
            if line_num % 4 == 1:  # Header lines
                headers.append(line.strip())
            if len(headers) >= num_reads:
                break
    return headers

def extract_read_id(header):
    """Extract the core read ID, handling various formats."""
    # Remove lane info if present
    header = header.split(' ')[0]
    # Remove /1 or /2 suffix if present
    if header.endswith('/1') or header.endswith('/2'):
        header = header[:-2]
    # Remove .1 or .2 suffix if present
    if header.endswith('.1') or header.endswith('.2'):
        header = header[:-2]
    return header

def validate_lane_pair(r1_file, r2_file):
    """Validate that R1 and R2 files for a lane have matching read names."""
    print(f"Checking pair: {os.path.basename(r1_file)} and {os.path.basename(r2_file)}")
    
    headers1 = read_fastq_headers(r1_file)
    headers2 = read_fastq_headers(r2_file)
    
    if len(headers1) != len(headers2):
        print(f"  ERROR: Files have different number of reads ({len(headers1)} vs {len(headers2)})")
        return False
    
    mismatches = 0
    for i, (h1, h2) in enumerate(zip(headers1, headers2)):
        id1 = extract_read_id(h1)
        id2 = extract_read_id(h2)
        
        if id1 != id2:
            if mismatches < 5:
                print(f"  Mismatch at read {i+1}: {h1} vs {h2}")
            mismatches += 1
    
    if mismatches > 0:
        print(f"  FAILED: Found {mismatches} mismatched read names")
        return False
    
    print("  PASSED: Read names are properly paired")
    return True

def find_lane_pairs(directory, sample_name=None):
    """Find all R1/R2 pairs for a sample across multiple lanes."""
    if not os.path.isdir(directory):
        directory = os.path.dirname(directory) or '.'
    
    # Get all fastq files
    fastq_files = glob.glob(f"{directory}/*.fastq.gz") + glob.glob(f"{directory}/*.fq.gz")
    
    # Filter by sample name if provided
    if sample_name:
        fastq_files = [f for f in fastq_files if sample_name in os.path.basename(f)]
    
    # Group by lane and read
    lane_pairs = {}
    for fastq in fastq_files:
        basename = os.path.basename(fastq)
        
        # Try to extract lane and read information
        lane_match = re.search(r'L00([1-4])', basename)
        read_match = re.search(r'R([12])', basename)
        
        if lane_match and read_match:
            lane = lane_match.group(1)
            read = read_match.group(1)
            
            if lane not in lane_pairs:
                lane_pairs[lane] = {}
            lane_pairs[lane][read] = fastq
    
    # Create pairs
    valid_pairs = []
    for lane, reads in lane_pairs.items():
        if '1' in reads and '2' in reads:
            valid_pairs.append((reads['1'], reads['2']))
    
    return valid_pairs

def validate_all_lanes(directory, sample_name=None):
    """Validate all lane pairs for a sample."""
    lane_pairs = find_lane_pairs(directory, sample_name)
    
    if not lane_pairs:
        print(f"No lane pairs found in {directory}" + 
              (f" for sample {sample_name}" if sample_name else ""))
        return False
    
    print(f"Found {len(lane_pairs)} lane pairs to validate")
    
    all_valid = True
    for r1, r2 in lane_pairs:
        valid = validate_lane_pair(r1, r2)
        all_valid = all_valid and valid
        print("")
    
    if all_valid:
        print("All lane pairs passed validation!")
    else:
        print("Some lane pairs failed validation. Check errors above.")
    
    return all_valid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <fastq_directory> [sample_name]")
        sys.exit(1)
    
    directory = sys.argv[1]
    sample_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = validate_all_lanes(directory, sample_name)
    sys.exit(0 if result else 1)
#!/usr/bin/env python3

import gzip
import os
import sys
import glob
import re

def read_fastq_headers(file_path, num_reads=1000):
    """Read headers from FASTQ file."""
    headers = []
    with gzip.open(file_path, 'rt') if file_path.endswith('.gz') else open(file_path, 'r') as f:
        line_num = 0
        for line in f:
            line_num += 1
            if line_num % 4 == 1:  # Header lines
                headers.append(line.strip())
            if len(headers) >= num_reads:
                break
    return headers

def extract_read_id(header):
    """Extract the core read ID, handling various formats."""
    # Remove lane info if present
    header = header.split(' ')[0]
    # Remove /1 or /2 suffix if present
    if header.endswith('/1') or header.endswith('/2'):
        header = header[:-2]
    # Remove .1 or .2 suffix if present
    if header.endswith('.1') or header.endswith('.2'):
        header = header[:-2]
    return header

def validate_lane_pair(r1_file, r2_file):
    """Validate that R1 and R2 files for a lane have matching read names."""
    print(f"Checking pair: {os.path.basename(r1_file)} and {os.path.basename(r2_file)}")
    
    headers1 = read_fastq_headers(r1_file)
    headers2 = read_fastq_headers(r2_file)
    
    if len(headers1) != len(headers2):
        print(f"  ERROR: Files have different number of reads ({len(headers1)} vs {len(headers2)})")
        return False
    
    mismatches = 0
    for i, (h1, h2) in enumerate(zip(headers1, headers2)):
        id1 = extract_read_id(h1)
        id2 = extract_read_id(h2)
        
        if id1 != id2:
            if mismatches < 5:
                print(f"  Mismatch at read {i+1}: {h1} vs {h2}")
            mismatches += 1
    
    if mismatches > 0:
        print(f"  FAILED: Found {mismatches} mismatched read names")
        return False
    
    print("  PASSED: Read names are properly paired")
    return True

def find_lane_pairs(directory, sample_name=None):
    """Find all R1/R2 pairs for a sample across multiple lanes."""
    if not os.path.isdir(directory):
        directory = os.path.dirname(directory) or '.'
    
    # Get all fastq files
    fastq_files = glob.glob(f"{directory}/*.fastq.gz") + glob.glob(f"{directory}/*.fq.gz")
    
    # Filter by sample name if provided
    if sample_name:
        fastq_files = [f for f in fastq_files if sample_name in os.path.basename(f)]
    
    # Group by lane and read
    lane_pairs = {}
    for fastq in fastq_files:
        basename = os.path.basename(fastq)
        
        # Try to extract lane and read information
        lane_match = re.search(r'L00([1-4])', basename)
        read_match = re.search(r'R([12])', basename)
        
        if lane_match and read_match:
            lane = lane_match.group(1)
            read = read_match.group(1)
            
            if lane not in lane_pairs:
                lane_pairs[lane] = {}
            lane_pairs[lane][read] = fastq
    
    # Create pairs
    valid_pairs = []
    for lane, reads in lane_pairs.items():
        if '1' in reads and '2' in reads:
            valid_pairs.append((reads['1'], reads['2']))
    
    return valid_pairs

def validate_all_lanes(directory, sample_name=None):
    """Validate all lane pairs for a sample."""
    lane_pairs = find_lane_pairs(directory, sample_name)
    
    if not lane_pairs:
        print(f"No lane pairs found in {directory}" + 
              (f" for sample {sample_name}" if sample_name else ""))
        return False
    
    print(f"Found {len(lane_pairs)} lane pairs to validate")
    
    all_valid = True
    for r1, r2 in lane_pairs:
        valid = validate_lane_pair(r1, r2)
        all_valid = all_valid and valid
        print("")
    
    if all_valid:
        print("All lane pairs passed validation!")
    else:
        print("Some lane pairs failed validation. Check errors above.")
    
    return all_valid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <fastq_directory> [sample_name]")
        sys.exit(1)
    
    directory = sys.argv[1]
    sample_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = validate_all_lanes(directory, sample_name)
    sys.exit(0 if result else 1)
