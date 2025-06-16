import os

def delete_all_todd_files():
    output_dir = "./outputs"
    n = 1
    deleted_any = False

    while True:
        before_file = os.path.join(output_dir, f"polynomial-before-todd-{n}.txt")
        after_file = os.path.join(output_dir, f"polynomial-after-todd-{n}.txt")
        after_read_file = os.path.join(output_dir, f"polynomial-after-todd-{n}-read.txt")

        found = False

        for file_path in [before_file, after_file, after_read_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                found = True
                deleted_any = True

        if not found:
            break

        n += 1

    if not deleted_any:
        print("No files were deleted.")

if __name__ == "__main__":
    delete_all_todd_files()
