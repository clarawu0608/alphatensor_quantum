import os

def rename_read_files():
    output_dir = "./outputs"
    n = 1

    while True:
        src = os.path.join(output_dir, f"polynomial-after-todd-{n}-read.txt")
        dst = os.path.join(output_dir, f"polynomial-after-todd-{n}.txt")

        if not os.path.exists(src):
            print(f"No more '-read' files to rename. Stopped at N={n}.")
            break

        os.rename(src, dst)
        print(f"Renamed: {src} → {dst}")
        n += 1

if __name__ == "__main__":
    rename_read_files()
