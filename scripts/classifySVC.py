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

    file_clf = 'classifiers/VOA-' + target + '.pkl'
    file_vec = 'classifiers/VOA-' + target + '.vec'

    try:
        lin_clf = pickle.load(open(file_clf))
        vec = pickle.load(open(file_vec))
        test_feat = vec.transform(test_featureDict)

        decoy = lin_clf.predict(test_feat)
        return decoy

    except IOError:
        raise 'NO_TARGET'

