import os
import hashlib

def sha256(filepath):
    with open(filepath, 'rb') as f:
        return int(hashlib.file_digest(f, 'sha256').hexdigest(), 16)

def walk_error(error):
    print(f'Error: {error.strerror}')

def main():
    encountered_hashes = dict()

    start_path = input("Start path > ");
    for root, _, files in os.walk(start_path):
        for f in files:
            path = os.path.join(root, f)
            digest = sha256(path)
            if digest in encountered_hashes:
                print(encountered_hashes[digest] + " and " + path)
            else:
                encountered_hashes[digest] = path 


if __name__ == '__main__':
    main()
