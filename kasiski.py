# -*- coding: utf-8 -*-
import string
import argparse
import sys

from vigenere import decrypt

NON_PRINTABLE_CHARS = "".join(map(lambda x: chr(x), range(0,31)+[127]))
CHARSET_SIZE = 128
MAX_KEY_LENGTH = 10

# command line argument parser configuration
def make_parser():
    parser = argparse.ArgumentParser(prog="kasiski")
    parser.add_argument('file', type=file)
    parser.add_argument('-t', '--typical-file', type=file)
    parser.add_argument('-m', '--most-frequent-char', type=str)
    parser.add_argument('-s', '--simple-guess', action="store_true")
    parser.add_argument('-i', '--icm-guess', action="store_true")
    return parser

# some argument combinations are not supported
def check_valid_args(args):
    if args.simple_guess & args.icm_guess:
        sys.exit("please choose either the simple guess (-s) or the icm guess (-i) method")
    
    if (args.most_frequent_char != None) & (args.typical_file != None):
        sys.exit("please choose either most frequent char (-m) or typical file (-t) as the key guessing assumption")

    if (args.most_frequent_char != None) :
        if len(args.most_frequent_char) > 1:
            sys.exit("argument of most_frequent_char option should be a single character. Got a String of 2+ characters")


# given a ciphertext, find the most likely keyword length
# given a ciphertext, find the most likely keyword length
# by computing the index of coincidence for each possible lentgth
def findKeyLength(cipher):
    lengths_coinc_idxs = []
    for l in range(1,MAX_KEY_LENGTH):
        
        subseqs_coinc_idxs = []

        subseqs = [""] * l                   # initialize l empty subseqs
        for a in range(0,l):
          subseqs[a] = cipher[a::l]          # from character index a take every l-th character in cipher
        
        for subseq in subseqs:
            subseqs_coinc_idxs.append(coinc_idx(subseq))    # compute index of coincidence of each sub sequence
        
        avg =  sum(subseqs_coinc_idxs)/float(len(subseqs))
        lengths_coinc_idxs.append(avg)
    
    maximum = max(lengths_coinc_idxs)
    return lengths_coinc_idxs.index(maximum)+1           # retain the length giving the higher ic across all its sub sequences

# computes the index of coincidence
def coinc_idx(substr):
    freqs = get_freqs(substr)
    return sum( map(lambda x: x*x, freqs) ) / float(len(substr)*len(substr))
    

# guesses a key by assuming mf is the most frequent character
def simple_guess(l,mf,cipher):
  key = ""
  for a in range(0,l):
    subseq = cipher[a::l]       # from character index a take every l-th character in cipher

    freqs = get_freqs(subseq)
    # for subseq i, the shift from its most frequent char and mf is the key i-th char
    key+=chr( ( freqs.index(max(freqs)) - ord(mf) )%128 )   
  return key
      

# given a cipher text and a key length guesses the gaps between char 0 
# and the remaining chars of the key using the icm method
def icm_guess(l,cipher):
  freqs = []                # frequencies of each sub sequences
  shift = []
  keyshifts = []
  for a in range(0,l):
    subseq = cipher[a::l]   # from character index a take every l-th character in cipher
    freqs.append(get_freqs(subseq))
    icms = []
    for sh in range(0,128):
      icms.append(icm(freqs[0], freqs[a]))   # compute icm between shifted freqs of sub seq i and freqs of sub seq 0
      freqs[a].append(freqs[a].pop(0))        # shift subseq i by one char
    keyshifts.append(icms.index(max(icms))) # retain the shift giving the higher icm
  return keyshifts
    

# computes the icm between strings x and y
def icm(x,y):
    lx = float(len(x))
    ly = float(len(y))
    return sum( map(lambda (a,b): (a/lx) * (b/ly), zip(x,y)) ) / lx*ly

# given a set of possible keys, a cipher text and a typical plain text, 
# guesses the most likely key by decrypting the cipher text
# and computing the icm between the obtained plain 
# text and the provided typical plain text 
def icm_shift_guess(keys, cipher_text, typ_file):
    icms = []
    for k in keys:
        plain = vigenere.decrypt(cipher_text, k)
        icms.append(icm(plain, typ_file))
    return keys[icms.index(max(icms))]          # return the key maximising the icm

# given a cipher text, the character shifts of the key and the most
# frequent character in the plain text, guesses the key by assuming
# the most frequent character in the first sub sequence is mf encoded
def mf_shift_guess(mf, cipher_text, keyshifts):
    subseq0 = cipher_text[0::len(keyshifts)]    # sub sequence 0
    freqs = get_freqs(subseq0)              
    shift0 = ( freqs.index(max(freqs)) - ord(mf) )%CHARSET_SIZE         # shift between mf and most freq char in sub seq 0
    return "".join(map(lambda c: chr((c+shift0)%CHARSET_SIZE),keyshifts))   # apply shift0 to all character shifts of the key

# given a string returns an array freqs of size CHARSET_SIZE where
# freqs[i] is the number of occurence of character index i in the
# ASCII table
def get_freqs(s):
    freqs = [0] * CHARSET_SIZE
    for ch in s:
      freqs[ord(ch)]+=1
    return freqs

# returns most frequent char of a string
def get_most_freq(s):
    freqs = get_freqs(s)
    return chr(freqs.index(max(freqs)))

# does s have any non printable characters
def has_non_printable_char(s):
    return reduce(lambda c,d: c | d, map(lambda e: e in NON_PRINTABLE_CHARS, s))


# computes all strings having keyshifts shifts between the first
# and the remaining characters
def possible_keys(keyshifts):
    # get all strings with char[i] shifted keyshifts[i] from char[0]
    keys = map(lambda y: ''.join(map(lambda x: chr((x+y)%CHARSET_SIZE), keyshifts)),range(32,127))

    # remove keys having non printable characters
    return filter( lambda s: not has_non_printable_char(s),keys)



# command line argument parsing 
arg_parser = make_parser();
cmd_args = sys.argv[1:]  
args = arg_parser.parse_args(cmd_args)
check_valid_args(args)

# read the given file
cipher_text = args.file.read()

# compute the most likely length
l = findKeyLength(cipher_text)          
print("found key of length {:d}".format(l))

if args.simple_guess:
    # perform simple guess

    # get the most frequent char
    if args.most_frequent_char != None :
        mf = args.most_frequent_char
    elif args.typical_file != None :
        mf = get_most_freq(args.typical_file.read())
    else:
        mf = ' '

    # guess the key
    key = simple_guess(l,mf,cipher_text)

else:
    # perform icm guess

    keyshifts = icm_guess(l,cipher_text)
    
    possible_keys = possible_keys(keyshifts)
    print("Possible keys :")
    for k in possible_keys:
        print k

    if args.typical_file != None :
        # guess the correct shifts using a typical plain text file
        key = icm_shift_guess(possible_keys, args.typical_file.read())
    else:
        # guess the correct shifts using the most frequent char
        if args.most_frequent_char != None :
            mf = args.most_frequent_char
        else:
            mf = ' '
        key = mf_shift_guess(mf,cipher_text,keyshifts)
    
print("most probable key is "+key)


