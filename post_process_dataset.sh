#!/bin/bash

cat train/train/part-*.csv | sed s/\|/\ \|/g > train_full.fw
cat test/test/part-*.csv | sed s/\|/\ \|/g | sed s/^A/\|A/g > test.fw

head -n 69713384 train_full.fw > train.fw
tail -n +69713385 train_full.fw > dev.fw

head -n 1000 train_full.fw > sample.fw

cat train.fw |awk -F "|" '{print $1}' > train_lables
cat dev.fw |awk -F "|" '{print $1}' > dev_labels

gzip *.fw

