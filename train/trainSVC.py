#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke Sakaguchi"

import sys
import os
import datetime
import re
import cPickle as pickle
import argparse
import numpy as np
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', action='store', dest='arg_f',
        help='label_feature', required=True)
arg_parser.add_argument('-k', action='store_true', dest='arg_k',
        help='k-best?', required=False)

args = arg_parser.parse_args()

target_list = []
all_label_feats = []

f = open('../data/target_verbs06', 'r')
for w in f:
    target_list.append(w.rstrip())
    all_label_feats.append([])

def train(filename):
    f = pickle.load(open(filename))
    for label_feature in f:
        try:
            target_id = target_list.index(label_feature[0])
            all_label_feats[target_id].append(label_feature[1])
        except ValueError:
            pass

    for word, all_lab_feat in zip(target_list, all_label_feats):
        labels = []
        feats = []

        for label_feature in all_lab_feat:
            labels.append(label_feature[0])
            feats.append(label_feature[1])

        target_label_feats = (labels, feats)

        try:
            vec = DictVectorizer()
            feats_vec = vec.fit_transform(feats)
            if args.arg_k:
                kbest_clf = svm.SVC(probability=True)
                kbest_clf.fit(feats_vec, labels)
                filename = '../classifiers_kbest/' + args.arg_f.split('/')[1].split('-')[0] + '-' + word
                pickle.dump(kbest_clf, open(filename + '.pkl', 'w')) 
                pickle.dump(vec, open(filename + '.vec', 'w')) 
            else:
                lin_clf = svm.LinearSVC()
                lin_clf.fit(feats_vec, labels)
                filename = '../classifiers/' + args.arg_f.split('/')[1].split('-')[0] + '-' + word
                pickle.dump(lin_clf, open(filename + '.pkl', 'w')) 
                pickle.dump(vec, open(filename + '.vec', 'w')) 
            
        except ValueError:
            pass

    return

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    train(args.arg_f)
    end_time = datetime.datetime.now()
    print "total elapsed time: " + str((end_time - start_time))
