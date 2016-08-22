# Semantic Distracotor Generator

Data used in my 2013 ACL paper, "Discriminative Approach to Fill-in-the-Blank Quiz Generation for Language Learners"

Keisuke Sakaguchi (keisuke[at]cs.jhu.edu)
Last updated: August, 2016

Note: The codebase is now compatible with the latest sklearn package. I recommend to use [Anaconda](https://www.continuum.io/downloads) as a platform.

- - -
This document describes the proposed method (DiscSimESL) described in my 2013 ACL paper:

    @InProceedings{sakaguchi-arase-komachi:2013:Short,
    author    = {Sakaguchi, Keisuke  and  Arase, Yuki  and  Komachi, Mamoru},
    title     = {Discriminative Approach to Fill-in-the-Blank Quiz Generation for Language Learners},
    booktitle = {Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
    month     = {August},
    year      = {2013},
    address   = {Sofia, Bulgaria},
    publisher = {Association for Computational Linguistics},
    pages     = {238--242},
    url       = {http://www.aclweb.org/anthology/P13-2043}
    }

It includes sample data and scripts to generate a fill-in-the-blank quiz with a semantic distractor for a given sentence which contains a target word.
We focus on 689 major verbs extracted from the Lang-8 Learner Corpora (http://cl.naist.jp/nldata/lang-8/) as targets.

N.B.

- There are 689 target verbs extracted from the Lang-8 Corpus, but the DiscSimESL covers 679.
- It does not include the original Lang-8 and VOA (Voice of America) data due to licensing restrictions.
- Classifiers for K-best quiz generation are not uploaded due to the data size (=18G). If you are interested in, please e-mail me.

## Pre-requisites
The scripts basically run on Python(2.7+).
Some Python modules and the [Stanford CoreNLP](http://www-nlp.stanford.edu/software/corenlp.shtml) toolkit are necessary to run the program. 


1. [lxml](http://lxml.de/)
2. [numpy](http://www.numpy.org/)
3. [scikit-learn](http://scikit-learn.org/stable/)
4. [pattern.en](http://www.clips.ua.ac.be/pages/pattern-en)

I recommend [Anaconda](https://www.continuum.io/downloads), which includes all the packages above.

N.B.
For Windows (x64) users, you may download Python [here](http://www.python.org/getit/) and find x64 extension packages for lxml and scikit-learn [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/). Currently, easy_install, pip, etc. don't support these python modules for Windows (x64).


## Generating semantic distractors
1. Download the codebase for generating semantic distractors, which is available at Github. If you are not familiar with git/github, please install git following the instruction [here](http://git-scm.com/book/en/Getting-Started-Installing-Git).

    `` git clone git@github.com:keisks/disc-sim-esl.git ``
    or
    `` git clone https://github.com:keisks/disc-sim-esl.git ``
    or
    You can download the zip file on the right side.


        > tree -L 1
            .
           ├── README.md         # This file
           ├── classifiers       # Classifiers for each verb
           ├── classifiers_kbest # K-best classifiers for each verb (blank)
           ├── data              # Confusion matrix
           ├── generate.py       # Main script
           ├── generate_kbest.py # Main script for K-best output
           ├── quiz_src          # Source files for quizzes
           ├── sample.txt        # Sample text file for a quiz
           ├── scripts           # Subscrips
           └── train             # Scrips for training



2. Parse *.txt file that contains sentences for quizzes. We use [Stanford CoreNLP](http://www-nlp.stanford.edu/software/corenlp.shtml) and put the output xml file into quiz_src/xml directory. (The dcoref option is not necessary.)

        Input: sample.txt
        Run: java -cp stanford-corenlp-1.3.5.jar:stanford-corenlp-1.3.5-models.jar:xom.jar:joda-time.jar:jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -file sample.txt -outputDirectory quiz_src/xml/
        Output: quiz_src/xml/sample.txt.xml


3. Execute generate.py to generate quiz sentences and options.
 This script will produce quiz sentences in quiz\_src/questions, and quiz options in quiz\_src/answer\_distractor.

        Run: python generate.py or generate_kbest.py
        Output:
        quiz_src/questions/sample.question
        quiz_src/questions/sample.answer
        quiz_src/answer_distractor/sample.txt.ans_dist
        quiz_src/answer_distractor/sample.txt.ans_dist_kbest
        (Kbest distractors are ranked by log-probability.)


## Training your own classifiers
1. Prepare xml files (parsed by Stanford CoreNLP). Here, for example, the xml files are located train/voa\_train\_test/small/.


2. Extract features from the corpus.

        cd train
        python feature_extract_VOA.py -x voa_train_test/small/

   The feature file is saved as models/VOA-feat.pkl 

3. Train classifiers for each verb. (SVM)

        python trainSVC.py -f models/VOA-feat.pkl (for 1-best classifiers)
        python trainSVC.py -f models/VOA-feat.pkl -k (for k-best classifiers)

   The classifiers (pickled) are saved at ./classifiers/ or ./classifiers_kbest/
        
   N.B. K-best classifiers take very long time to train (several hours/verb) in average, and parallel execution (by splitting target_verb) is highly recommended.


- - -
If you have any questions, please email me (keisuke[at]cs.jhu.edu).