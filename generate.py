#!/usr/bin/env python
#encoding: utf-8

__author__ = ""
__version__ = ""
__copyright__ = ""
__license__ = ""
__descripstion__ = ""
__usage__ = ""

import sys
import os
import datetime
import re
import random
import scripts.stanfordXmlParser
import scripts.word_regularize
import scripts.classifySVC


##### edit here according to your environments #####
sys.path.append("/work/keisuke-sa/proj/msra2012/discriminative/src/pattern-2.4/")
from pattern.en import *
#========================


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

        #ここにquestionfileをつくる
        print 'Generating for: ' + filename
        out_q = open('quiz_src/question/' + filename.split('.xml')[0] + '.question', 'w')
        out_d = open('quiz_src/distractor_answer/' + filename.split('.xml')[0] + '.dist_ans', 'w')

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

                            #inflect decoy according to target's POS                            

                            # VBD
                            if sentDict['pos'][i] == 'VBD':
                                decoy = conjugate(decoy, 'p') 

                            # VBP
                            elif sentDict['pos'][i] == 'VBP':
                                decoy = conjugate(decoy, '1sg') 

                            # VBZ
                            elif sentDict['pos'][i] == 'VBZ':
                                decoy = conjugate(decoy, '3sg') 

                            # VBG
                            elif sentDict['pos'][i] == 'VBG':
                                decoy = conjugate(decoy, 'part') 

                            # VBN
                            elif sentDict['pos'][i] == 'VBN':
                                decoy = conjugate(decoy, 'ppart') 


                            #wirte quiz sentence 

                            for j, w in enumerate(sentDict['word']):
                                if i != j:
                                    try:
                                        out_q.write(w + ' ')
                                    except UnicodeEncodeError:
                                        out_q.write('NON-ASCII ')
                                else:
                                    out_q.write('_____' + ' ')
                            out_q.write('\n')

                            out_d.write(decoy + ' ' + sentDict['word'][i] + '\n')
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

    print "Complete!!"
    return

if __name__ == '__main__':
    generate_question()

