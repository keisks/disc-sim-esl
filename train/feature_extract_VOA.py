#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke Sakaguchi"

import sys
import os
import datetime
import re
import random
import cPickle as pickle
import argparse
import scripts.stanfordXmlParser as stanfordXmlParser
import scripts.word_regularize as word_regularize

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-x', action='store', dest='arg_x',
        help='xml_directory', required=True)
#arg_parser.add_argument('-w', action='store', dest='arg_w',
#        help='target Word list', required=True)
#arg_parser.add_argument('-m', action='store', dest='arg_c',
#        help='confusion matrix (3gramProbMatSelect.txt)', required=True)

args = arg_parser.parse_args()

# make conf matrix
confDict = {}
#f = open(args.arg_c, 'r')
f = open('./3gramProbMatSelect.txt', 'r')
for entry in f:
    triple = entry.split(' ')
    if triple[0] in confDict:
        confDict[triple[0]][0].append(triple[1])
        confDict[triple[0]][1].append(triple[2].rstrip())

    else:
        confDict[triple[0]] = ([],[])
        confDict[triple[0]][0].append(triple[1])
        confDict[triple[0]][1].append(triple[2].rstrip())

#print confDict

targets = {}
#f = open(args.arg_w, 'r')
f = open('../data/target_verbs', 'r')

for w in f:
    targets[w.rstrip()] = 1

def choose(candidates, probabilities):
    probabilities = [float(x) for x in probabilities]
    probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
    if probabilities[-1] > 1.0:
        probabilities = [x/probabilities[-1] for x in probabilities]
    rand = random.random()
    for candidate, probability in zip(candidates, probabilities):
        if rand < probability:
            return candidate
    return None


def generate_label(word):
    label_feat = confDict[word] #tuple of lists ([feats1, ...] [probs1, ...])
    #print label_feat

    label_list = []
    for i in range(100):
        pseudo_label = choose(label_feat[0], label_feat[1])
        label_list.append(pseudo_label)
    
    return label_list


def doit(dirpath):
    filenames = os.listdir(dirpath)
    label_feature_all = []
    for f in filenames:
        #fileID = int(f.split('lang8_')[1].split('.txt')[0])
        parsedSentList = stanfordXmlParser.parseXml(dirpath + f)

        for sentDict in parsedSentList:
            #print sentDict['lemma']
            #print sentDict['basDep']

            for i, lem in enumerate(sentDict['lemma']):
                if lem in targets:
                    feature_dict = {}

                    # dependency featureを取得
                    for dependency in sentDict['basDep']:
                        if dependency[1] == i:
                            dependent = word_regularize.regularize(sentDict['lemma'][dependency[2]])
                            feature_dict[dependency[0]] = dependent
                            #featDep = dependency[0] + '_' + dependent
                    
                    try:
                        feature_dict['w-1'] = sentDict['lemma'][i-1]    #previous word
                    except IndexError:
                        pass
                    
                    try:
                        feature_dict['w-2'] = sentDict['lemma'][i-2]
                    except IndexError:
                        pass
                    
                    try:
                        feature_dict['w+1'] = sentDict['lemma'][i+1] #following word
                    except IndexError:
                        pass
                    
                    try:
                        feature_dict['w+2'] = sentDict['lemma'][i+2]
                    except IndexError:
                        pass

                    label_list = generate_label(lem)
                    
                    for label in label_list:
                        #print lem, (label, feature_dict) # for intermediate use
                        label_feature_all.append([lem, (label, feature_dict)])

    return label_feature_all

if __name__ == '__main__':
    # For logging date and time
    start_time = datetime.datetime.now()
    #print "start at: " + str(start_time)
    
    #log_file = open(exp_time + '_' + str(argvs[0]) + '.log', 'w')
    #log_file.write('script_name: ' + str(argvs) + '\n')
    #log_file.write('start at: ' + str(start_time) + '\n')
    
    # For module tests, write code here.

    out = doit(args.arg_x)
    pickle.dump(out, open('./models/VOA-feat.pkl', 'w'))
    
    # For logging date and time
    end_time = datetime.datetime.now()
    #print "end at: " + str(end_time)
    print "total elapsed time: " + str((end_time - start_time))
    #log_file.write('end at: ' + str(end_time) + '\n')
    #log_file.write('total elapsed time: ' + str((end_time - start_time)) + '\n')

