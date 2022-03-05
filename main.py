from ImageLib import ImageLib
import sys
import os
import errno

def create_path(dirToBeCreated):
    if not os.path.exists(os.path.dirname(dirToBeCreated)):
        try:
            os.makedirs(os.path.dirname(dirToBeCreated))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

src_dir = sys.argv[1]
src_dir = os.path.abspath(src_dir)
dest_dir = src_dir + "_Squared"

for root, dirs, files in os.walk(src_dir):
    for file in files:
        src_file_path = os.path.abspath(os.path.join(root, file))
        dest_file_path  = src_file_path.replace(src_dir, dest_dir)
        create_path(dest_file_path)
        img = ImageLib(src_file_path).get_squared_image()
        img.save(dest_file_path)
        print(file +": DONE")
