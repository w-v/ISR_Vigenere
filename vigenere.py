import string

plainfile = 'plain.txt'
cryptfile = 'crypt.txt'

key = 'nigger'

def crypt(plain, cipher, key):
    with open(cipher, "w") as cipher_file:
        with open(plain, "r") as plain_file:
            i = 0
            while True:
                c = plain_file.read(1)
                if not c:
                    print "End of file"
                    break
                print(key[i%len(key)])
                cipher_file.write(charcrypt(c,key[i%len(key)]));
                print "writing"
                i+=1
        plain_file.close()
    cipher_file.close()

def decrypt(plain, cipher, key):
    with open(cipher, "r") as cipher_file:
        with open(plain, "w") as plain_file:
            i = 0
            while True:
                c = cipher_file.read(1)
                if not c:
                    print "End of file"
                    break
                plain_file.write(chardecrypt(c,key[i%len(key)]));
                i+=1

def charcrypt(c,k):
    return chr((ord(c)+ord(k))%128)
    
def chardecrypt(c,k):
    return chr((ord(c)-ord(k))%128)

  

crypt(plainfile, cryptfile, key)
decrypt('decrypt.txt', cryptfile, key)

