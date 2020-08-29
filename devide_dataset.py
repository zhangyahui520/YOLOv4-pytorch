#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : pycharm
#   File name   : devide_dataset.py
#   Author      : 张亚辉
#   Created date: 2019-07-19 10:58:26
#   Description :
#       对数据集进行划分，并读取为path， Bbox， class格式文件
#
#================================================================

import os
import random


def split_dataset(xmlfilepath, train_percent, year, root_dir=None):
    if root_dir is None:
        root_dir = os.getcwd()
    total_xml = os.listdir(xmlfilepath)
    num = len(total_xml)
    train = random.sample(total_xml, int(train_percent * num))
    test = list(set(total_xml).difference(set(train)))
    ftest = open('{}/VOCdevkit/VOC{}/ImageSets/Main/test.txt'.format(root_dir, year), 'w')
    ftrain = open('{}/VOCdevkit/VOC{}/ImageSets/Main/train.txt'.format(root_dir, year), 'w')

    for file in train:
        # name = file.split('.')[0] + '\n'
        # 因为新处理的文件中带有“。”， 需要修改处理方法
        name = file[:-4] + '\n'
        ftrain.write(name)
    for file in test:
        # name = file.split('.')[0] + '\n'
        name = file[:-4] + '\n'
        ftest.write(name)


    print('按照训练集比例为{}来划分文件夹{}'.format(str(train_percent), xmlfilepath))
    ftrain.close()
    ftest.close()
    return train, test


if __name__ == '__main__':
    train_percent = 0.8
    # xmlfilepath = 'VOCdevkit/VOC2012/Annotations'
    xmlfilepath = 'VOCdevkit/VOC2012/Annotations'
    train, test = split_dataset(xmlfilepath, train_percent, year=2007)

