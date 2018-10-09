# Vigenere's cipher and cryptanalysis

## Vigenere's cipher

```
usage: vigenere [-h] {c,d} file_in file_out key

positional arguments:
  {c,d}       c for encrypting, d for decrypting
  file_in     input file
  file_out    output file
  key

optional arguments:
  -h, --help  show this help message and exit
```

## Kasiski's cryptanalysis

 ``` 
 usage: kasiski [-h] [-t TYPICAL_FILE] [-m MOST_FREQUENT_CHAR] [-s] [-i] file

positional arguments:
  file                  file on which the cryptanalysis is performed

optional arguments:
  -h, --help            show this help message and exit
  -t TYPICAL_FILE, --typical-file TYPICAL_FILE
                        plain text file of similar character distribution than
                        the encrypted plain text. With icm guess (-i), is used
                        to guess the offset of the key's first character given
                        the shifts of every character to the first one. Is
                        compared to the plaintext of every possible key by
                        computing their icm With simple guess (-s), is used to
                        compute the most frequent char Is not compatible with
                        -m
  -m MOST_FREQUENT_CHAR, --most-frequent-char MOST_FREQUENT_CHAR
                        most frequent character in the plain text, is used to
                        guess the key using simple guess, and to choose one
                        from possible keys using icm guess Is not compatible
                        with -t
  -s, --simple-guess    Guess the key using the simple guess method Only
                        assumes a most frequent character, and deduces the key
                        from that
  -i, --icm-guess       Guess the key using the icm guess method Actually try
                        and match frequency distributions of sub sequences
                        corresponding to key characters in order to find a set
                        of possible keys, then use the specified (default: -m
                        ' ') method to choose the most probable key```


