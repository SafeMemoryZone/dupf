import os
import hashlib
import argparse


def sha256(filepath):
    with open(filepath, "rb") as f:
        return int(hashlib.file_digest(f, "sha256").hexdigest(), 16)


def main():
    parser = argparse.ArgumentParser(
        prog="dupf",
        description="Simple script that finds duplicate files.",
    )

    parser.add_argument(
        "-r",
        "--root",
        type=str,
        help="path to the root directory (default is CWD)",
        default=os.getcwd(),
    )
    args = parser.parse_args()

    encountered_hashes = dict()
    duplicates_size = 0

    for root, _, files in os.walk(args.root):
        for f in files:
            path = os.path.join(root, f)

            if os.path.islink(path) or os.stat(path).st_nlink > 1:
                continue

            try:
                digest = sha256(path)
            except PermissionError:
                print(f"Warning: Unable to open {path} (permission error)")
                continue

            if digest in encountered_hashes:
                print(encountered_hashes[digest] + " and " + path)
                duplicates_size += os.path.getsize(path)
            else:
                encountered_hashes[digest] = path

    units = ["b", "kb", "mb", "gb"]
    convs = [1, 1000, 1000_000, 1000_000_000]

    best_idx = 0

    for i in range(len(convs)):
        conv = convs[i]
        curr = len(str(round(duplicates_size / conv, 1)))
        best = len(str(round(duplicates_size / convs[best_idx], 1)))
        if curr < best:
            best_idx = i

    print(
        f"\nFound ~{round(duplicates_size / convs[best_idx], 1)}{units[best_idx]} worth of duplicate files."
    )


if __name__ == "__main__":
    main()
