import os
import hashlib

def sha256(filepath):
    with open(filepath, 'rb') as f:
        return int(hashlib.file_digest(f, 'sha256').hexdigest(), 16)

def walk_error(error):
    print(f'Error: {error.strerror}')

def main():
    encountered_hashes = dict()
    duplicates_size = 0

    start_path = input("Start path > ");
    for root, _, files in os.walk(start_path):
        for f in files:
            path = os.path.join(root, f)
            digest = sha256(path)
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
    
    print(f'\nFound ~{round(duplicates_size / convs[best_idx], 1)}{units[best_idx]} worth of duplicate files.')


if __name__ == '__main__':
    main()
