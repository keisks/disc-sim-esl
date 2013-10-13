#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke Sakaguchi"
__version__ = "0.9"

import sys
import os
import datetime
import re
import cPickle as pickle
import numpy as np
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer

def classify(target, test_featureDict):

    file_clf = 'classifiers_kbest/VOA-' + target + '.pkl'
    file_vec = 'classifiers_kbest/VOA-' + target + '.vec'

    try:
        clf = pickle.load(open(file_clf))
        vec = pickle.load(open(file_vec))
        test_feat = vec.transform(test_featureDict)

        decoy = clf.predict(test_feat)
        log_proba = clf.predict_log_proba(test_feat)
        k_best = sorted(zip(log_proba[0], clf.classes_), reverse=True)
        return k_best

    except IOError:
        raise 'NO_TARGET'

