# -*- coding: utf-8 -*-
import string
import argparse
import sys

DEFAULT_KEY = 'noguess!'
CHARSET_SIZE = 128

# command line argument parser setup
def makeParser():
    parser = argparse.ArgumentParser(prog="vigenere")
    parser.add_argument('command', choices=['c', 'd'], help="c for encrypting, d for decrypting")
    parser.add_argument('file_in', type=argparse.FileType('r'), help="input file")              # Opens file and gives it in the object returned by parse_args()
    parser.add_argument('file_out', type=argparse.FileType('w'), help="output file")            #
    parser.add_argument('key', type=str, default=DEFAULT_KEY)
    return parser

# encrypt string plain with key using Vigenere's cipher
def encrypt(plain, key):
  i = 0
  s = ""
  for c in plain:
    s+=charencrypt(c,key[i%len(key)]);
    i+=1
  return s

# decrypt string cipher with key using Vigenere's cipher
def decrypt(cipher, key):
  i = 0
  s = ""
  for c in cipher:
    s+=chardecrypt(c,key[i%len(key)]);
    i+=1
  return s

def decrypt_file(plain, cipher, key):
    plain.write(decrypt(cipher.read(), key))

def encrypt_file(plain, cipher, key):
    cipher.write(encrypt(plain.read(), key))

# shifts char c forward by char k index in the ASCII table
def charencrypt(c,k):
    return chr((ord(c)+ord(k))%CHARSET_SIZE)

# shifts char c back by char k index in the ASCII table
def chardecrypt(c,k):
    return chr((ord(c)-ord(k))%CHARSET_SIZE)

if __name__ == '__main__':
    # do not run when being imported

    # command line argument parsing
    arg_parser = makeParser();
    cmd_args = sys.argv[1:]         # don't take the name of the script
    args = arg_parser.parse_args(cmd_args)

    if args.command == 'c':
        encrypt_file(args.file_in, args.file_out, args.key)
    else:
        decrypt_file(args.file_out, args.file_in, args.key)

    args.file_in.close()
    args.file_out.close()
