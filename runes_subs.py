#!/usr/bin/python
import random
import string
import enchant
import os
import sys
from tqdm import tqdm

"""
Cicada 3301 rune trial.
Trying to use simple substitute decoding.
Script uses encoded array of words, loops over it,
and then checks whether decoded string seems to be valid english word.

This version is single-threaded.
No optimization done yet.
"""


"""
////////////////////////////////
UTIL FUNCTIONS
////////////////////////////////
"""

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 3, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


class VoiceNotify(object):
    is_enabled = True

    @classmethod
    def say(cls, msg):
        if VoiceNotify.is_enabled:
            os.system('say -v "Vicki" "%s"' % msg)


def get_next_variant():
    """
    Returns new generated substitute sample from ascii_letters of size 30
    :return:
    """
    return ''.join(random.sample(string.printable, 30))


def print_decrypt_variant():
    """
    Function tries to apply generated substitute sample to decode encrypted data.
    It check whether at least 50% of words are in english dictionary
    :return:
    """
    decrypted_str = '' # will hold the merged result string
    rstr = get_next_variant()
    decrypted_word = ''
    words_detected = 0

    for word in enc_words:
        for i, j in enumerate(word['symbols']):

            if j in expectations:
                symb = expectations[j]
                #print('using expecto ', symb)
                #rstr[j] = symb
            else :
                symb = rstr[j]
            decrypted_word += symb

        if d.check(decrypted_word):
            words_detected += 1
        decrypted_str += ' ' + decrypted_word
        decrypted_word = ''

    # print alert if we have more than 50 percent
    # of words decoded
    if (words_detected / len(enc_words)) >= 0.3:
        print(decrypted_str + '  [' + rstr + ']')
        VoiceNotify.say("Found possible combination")

    # print alert and even stop if we found more than 80%
    # of data successfully decrypted
    if (words_detected / len(enc_words)) >= 0.5:
        print(decrypted_str + '  [' + rstr + ']')
        print('BESTBESTBESTBESTBESTBESTBESTBESTBESTBESTBEST')
        VoiceNotify.say("Found best detection!")
        return

"""
////////////////////////////////
MAIN LOGIC
////////////////////////////////
"""

# Initiating english vocabolary
d = enchant.Dict("en_US")
expectations = {
    12: 'a',
    30: 'v',
    25: 'o',
    20: 'w',
    8: 'y',


}
# These are coded words.
# Code is very simple: we assume that data is encrypted via substitute.
# Every number in word is a coded equivalent of encrypted symbol
enc_words = [
             {
                 'symbols': [29, 12, 20, 15, 5],
             },
             {
                 'symbols': [19, 14, 28],
             },
             {
                'symbols': [25, 24, 2, 11, 24, 19, 26, 12],
             },
             {
                'symbols': [14, 24],
             },
             {
                'symbols': [4, 1, 11, 25, 26],
             },
             {
                'symbols': [16, 9, 3, 24],
             },
             {
                'symbols': [16, 22, 24, 21],
             },
             {
                'symbols': [10, 26, 28, 23, 24],
             },
             {
                'symbols': [25, 22, 23],
             },
             {
                'symbols': [17, 16, 3, 19],
             },

             {
                'symbols': [20, 26, 27],
             },
             {
                 'symbols': [27, 5, 25, 9],
             },
             {
                'symbols': [19, 5, 17],
             },
]


#printProgress(0, 9999999999, prefix = 'P:', suffix = 'C', barLength = 80)
for k in tqdm(range(0, 9999999999)):
    #if k % 10 == 0:
    #    printProgress(k, 9999999999, prefix = 'P:', suffix = 'C', barLength = 80)
    print_decrypt_variant()
