import os
import shutil

def copy_polynomials():
    input_dir = "./outputs"
    n = 1

    while True:
        src = os.path.join(input_dir, f"polynomial-before-todd-{n}.txt")
        dst = os.path.join(input_dir, f"polynomial-after-todd-{n}.txt")

        if not os.path.exists(src):
            print(f"No more files to copy. Stopped at N={n}.")
            break

        shutil.copyfile(src, dst)
        print(f"Copied: {src} → {dst}")
        n += 1

if __name__ == "__main__":
    copy_polynomials()
