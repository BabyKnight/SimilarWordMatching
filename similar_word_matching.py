#!/usr/bin/python
"""A simple spell checker, return most similar_words list"""

import os, sys, subprocess, signal

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def found(word, args, cwd = None, shell = True):
    child = subprocess.Popen(args, 
        shell = shell,  
        stdin = subprocess.PIPE, 
        stdout = subprocess.PIPE, 
        cwd = cwd,  
        universal_newlines = True) 
    child.stdout.readline()
    (stdout, stderr) = child.communicate(word)
    if ": " in stdout:
        # remove \n\n
        stdout = stdout.rstrip("\n")
        # remove left part until :
        left, candidates = stdout.split(": ", 1) 
        candidates = candidates.split(", ")
        # making an error on the first letter of a word is less 
        # probable, so we remove those candidates and append them 
        # to the tail of queue, make them less priority
        for item in candidates:
            if item[0] != word[0]: 
                candidates.remove(item)
                candidates.append(item)
        return candidates
    else:
        return None

def correct(word):
    candidates1 = found(word, 'aspell -a')
    if not candidates1:
        print "Exact word match, No suggestion required !"
        return  

    print "No exact word match, suggestion list below: "
    print candidates1
    return candidates1

def similar_word_matching(word):
    correct(word)

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        input = raw_input()
        correct(input)


