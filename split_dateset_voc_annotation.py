#! /usr/bin/env python
# coding=utf-8
# ================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : pycharm
#   File name   : voc_annotation.py
#   Author      : 张亚辉
#   Created date: 2019-07-19 10:58:26
#   Description :
#   #按照train.txt读取xml中的坐标及类别， 生成path Bbox，class
# UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 30: illegal multibyte sequence
# in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id), 'rb')   增加‘rb’
#  先划分数据集，然后生成指定格式
#
# ================================================================
import os
import xml.etree.ElementTree as ET
from os import getcwd
from config import yolov4_config as cfg
from devide_dataset import split_dataset

classes = cfg.Customer_DATA['CLASSES']

def convert_annotation(year, image_id, list_file):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml' % (year, image_id), 'rb')

    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)),
             int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        print(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

def convert_pascal_to_yolo(year, precent, root=None):
    '''划分数据集并处理'''
    if root is None:
        root = getcwd()
    train_percent = precent
    xmlfilepath = '{}/VOCdevkit/VOC{}/Annotations'.format(root, year)
    split_dataset(xmlfilepath, train_percent, year)


    for image_set in ['train', 'test']:
        image_ids = open('{root}/VOCdevkit/VOC{year}/ImageSets/Main/{image_set}.txt'.format(root=root, year=year, image_set=image_set)).read().strip().split()
        list_file = open('{}_{}.txt'.format(year, image_set), 'w')
        for image_id in image_ids:
            img_path = '{}/VOCdevkit/VOC{}/JPEGImages/{}.jpg'.format(root, year, image_id)
            if os.path.exists(img_path):
                list_file.write(img_path)
                convert_annotation(year, image_id, list_file)
                list_file.write('\n')
            else:
                print('路径不存在： {}'.format(img_path))
        list_file.close()

if __name__ == '__main__':
    year = '2007'
    precent = 0.8
    convert_pascal_to_yolo(year, precent)