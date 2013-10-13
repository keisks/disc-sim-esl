#!/usr/bin/env python
#encoding: utf-8

__author__ = "Keisuke Sakaguchi"
__version__ = "0.9"

import sys
import os
import datetime
import re
import random
import scripts.stanfordXmlParser
import scripts.word_regularize
import scripts.classifySVC
import scripts.classifySVC_kbest

##### edit here according to your environments #####
path_to_pattern = "YOUR_PATH_TO_pattern.en (e.g. ./pattern-2.4/)"
#========================
sys.path.append(path_to_pattern)
from pattern.en import *


# target dictionary
targets = {}
f = open('data/target_verbs', 'r')
for w in f:
    targets[w.rstrip()] = 1

def inflection(pos, word):

    # VBD
    if pos == 'VBD':
        word_inflect = conjugate(word, 'p')

    # VBP
    elif pos == 'VBP':
        word_inflect = conjugate(word, '1sg')

    # VBZ
    elif pos == 'VBZ':
        word_inflect = conjugate(word, '3sg')

    # VBG
    elif pos == 'VBG':
        word_inflect = conjugate(word, 'part')

    # VBN
    elif pos == 'VBN':
        word_inflect = conjugate(word, 'ppart')

    else:
        word_inflect = word

    return word_inflect

def generate_question():

    file_list = os.listdir('quiz_src/xml/')
    print 'Start!!'

    for filename in file_list:
        filename_full = 'quiz_src/xml/' + filename
        parsedSentList = scripts.stanfordXmlParser.parseXml(filename_full)

        print 'Generating for: ' + filename
        out_q = open('quiz_src/question/' + filename.split('.xml')[0] + '.question', 'w')
        out_d = open('quiz_src/distractor_answer/' + filename.split('.xml')[0] + '.dist_ans', 'w')
        out_d_kbest = open('quiz_src/distractor_answer/' + filename.split('.xml')[0] + '.dist_ans_kbest', 'w')

        for sentDict in parsedSentList:
            generation_flag = 0     # Check if the sentence has a target or not, first.

            for word in sentDict['lemma']:
                if word in targets:
                    generation_flag = 1
                else:
                    pass

            if generation_flag == 1:

                decoy_made_flag = 0     #Avoid multiple blanks for one sentence.
                for i, target in enumerate(sentDict['lemma']):
                    if decoy_made_flag == 1:
                        pass
                    else:
                        if ((target in targets) and (sentDict['pos'][i][0] == 'V')):
                            feature_dict = {}

                            # get dependency features
                            for dependency in sentDict['basDep']:
                                if dependency[1] == i:
                                    dependent = scripts.word_regularize.regularize(sentDict['lemma'][dependency[2]])
                                    feature_dict[dependency[0]] = dependent
                            
                            target_pos = sentDict['pos'][i]
                            
                            try:
                                feature_dict['w-2'] = sentDict['lemma'][i-2]
                            except IndexError:
                                pass
         
                            try:
                                feature_dict['w-1'] = sentDict['lemma'][i-1]
                            except IndexError:
                                pass
                           
                            try:
                                feature_dict['w+1'] = sentDict['lemma'][i+1]
                            except IndexError:
                                pass
                            
                            try:
                                feature_dict['w+2'] = sentDict['lemma'][i+2]
                            except IndexError:
                                pass

                            #generate decoys 
                            decoy = scripts.classifySVC.classify(target, feature_dict)[0]
                            decoy_kbest = scripts.classifySVC_kbest.classify(target, feature_dict)

                            #inflect decoy according to target's POS                            
                            kbest_infl = []

                            # VBD
                            if sentDict['pos'][i] == 'VBD':
                                decoy = conjugate(decoy, 'p') 
                                for kbest in decoy_kbest:
                                    decoy_k = conjugate(kbest[1], 'p')
                                    kbest_infl.append(decoy_k)

                            # VBP
                            elif sentDict['pos'][i] == 'VBP':
                                decoy = conjugate(decoy, '1sg') 
                                for kbest in decoy_kbest:
                                    decoy_k = conjugate(kbest[1], '1sg')
                                    kbest_infl.append(decoy_k)

                            # VBZ
                            elif sentDict['pos'][i] == 'VBZ':
                                decoy = conjugate(decoy, '3sg') 
                                for kbest in decoy_kbest:
                                    decoy_k = conjugate(kbest[1], '3sg')
                                    kbest_infl.append(decoy_k)

                            # VBG
                            elif sentDict['pos'][i] == 'VBG':
                                decoy = conjugate(decoy, 'part') 
                                for kbest in decoy_kbest:
                                    decoy_k = conjugate(kbest[1], 'part')
                                    kbest_infl.append(decoy_k)

                            # VBN
                            elif sentDict['pos'][i] == 'VBN':
                                decoy = conjugate(decoy, 'ppart') 
                                for kbest in decoy_kbest:
                                    decoy_k = conjugate(kbest[1], 'ppart')
                                    kbest_infl.append(decoy_k)

                            #write quiz sentence 

                            for j, w in enumerate(sentDict['word']):
                                if i != j:
                                    try:
                                        out_q.write(w + ' ')
                                    except UnicodeEncodeError:
                                        out_q.write('NON-ASCII ')
                                else:
                                    out_q.write('_____' + ' ')
                            out_q.write('\n')

                            out_d.write(sentDict['word'][i] + '\t' + decoy + '\n')
                            out_d_kbest.write(sentDict['word'][i] + '\t')
                            for decoy_k, prob in zip(kbest_infl, decoy_kbest):
                                out_d_kbest.write(str(decoy_k) + ':' + str(prob[0]) + ',')
                            out_d_kbest.write('\n')
                            decoy_made_flag = 1

            else:
                for w in sentDict['word']:
                    try:
                        out_q.write(w + ' ')
                    except UnicodeEncodeError:
                        out_q.write('NON-ASCII ')
                out_q.write('\n')

        out_q.close()
        out_d.close()
        out_d_kbest.close()

    print "Complete!!"
    return

if __name__ == '__main__':
    generate_question()

