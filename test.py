def extract_best_t_counts(log_path, output_path):
    keyword = "Best T-count for nc_toff_3:"
    with open(log_path, 'r') as f:
        matches = [line.strip() for line in f if keyword in line]
    
    with open(output_path, 'w') as out:
        out.write("\n".join(matches))
    print(f"Extracted {len(matches)} lines to {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python extract_tcounts.py output.log filtered_tcounts.txt")
    else:
        log_file = sys.argv[1]
        out_file = sys.argv[2]
        extract_best_t_counts(log_file, out_file)
