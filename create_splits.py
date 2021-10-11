import argparse
import glob
import os
import random

import numpy as np

from utils import get_module_logger


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the 
    same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /mnt/data
    """
    dest_ratios = [("train", 0.7), ("validation", 0.2), ("test", 0.1)]

    tfRecordFiles = []
    for tfRecordFile in glob.glob(os.path.join(data_dir,'*.tfrecord')):
        tfRecordFiles.append(tfRecordFile)

    random.shuffle(tfRecordFiles)

    total_count = len(tfRecordFiles)
    cur_ratio = 0.0
    for dest_dir_name, ratio in dest_ratios:
        start_index = int(round(cur_ratio * total_count))
        cur_ratio += ratio
        end_index = int(round(cur_ratio * total_count))
        if end_index == total_count:
            end_index = None
        dest_dir = os.path.join(data_dir, dest_dir_name)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for tfRecordFile in tfRecordFiles[start_index : end_index]:
            os.rename(tfRecordFile, os.path.join(dest_dir, os.path.basename(tfRecordFile)))


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--data_dir', required=True,
                        help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)