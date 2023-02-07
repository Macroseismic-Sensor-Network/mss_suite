#! /usr/bin/env python3

import os
import time

# The directories to process and the corresponding time span
# in seconds for which to keep the files in the directory.
data_dir = {'/home/mss/mseed': 120,
            }

now = time.time()

# Process the data_dir folders.
for cur_data_dir, cur_span in data_dir.items():
    file_list = sorted([x for x in os.listdir(cur_data_dir) if os.path.isfile(os.path.join(cur_data_dir, x))])
    for cur_file in file_list:
        cur_filepath = os.path.join(cur_data_dir, cur_file)
        if os.stat(cur_filepath).st_mtime <= (now - cur_span):
            os.remove(os.path.join(cur_data_dir, cur_file))
