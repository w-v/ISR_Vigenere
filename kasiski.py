import string

cipher = 'crypt.txt'

def file2String(f):
    with open(f, 'r') as f:
        return f.read().replace('\n', '')

def findKeyLength(cipher):
    l_coinc_idx = []
    for l in range(1,10):
        chunks = [""] * l
        coinc_idxs = []
        for a in range(0,l):
          #print(a)
          chunks[a] = cipher[a::l]
        for chunk in chunks:
            coinc_idxs.append(coinc_idx(chunk))
        print(coinc_idxs)
        avg =  sum(coinc_idxs)/float(len(chunks)) 
        print(avg)
        l_coinc_idx.append(avg)
    maximum = max(l_coinc_idx)
    print(l_coinc_idx.index(maximum))
    print(maximum)
    return l_coinc_idx.index(maximum)+1

def coinc_idx(substr):
    freq = {}
    for c in substr:
        if not c in freq.keys():
            freq[c] = 0
        freq[c]+=1
    print(freq)
    return sum( map(lambda x: x*x, freq.values()) ) / float(len(substr)*len(substr))
    

def simpleguess(l,mf,cipher):
  key = ""
  print(cipher)
  for a in range(0,l):
    subseq = cipher[a::l]
    print(subseq)
    freqs = [0] * 128
    for ch in subseq:
      freqs[ord(ch)]+=1
    key+=chr( ( freqs.index(max(freqs)) - ord(mf) )%128 )
    print(freqs)
  print(key)
  return key
      

def ICMguess(l,cipher):
  freqs = []
  shift = []
  keyshifts = []
  for a in range(0,l):
    substr = cipher[a::l]
    freqs.append([0] * 128)
    for ch in substr:
      freqs[a][ord(ch)]+=1
    icms = []
    # make a copy
    shift = list(freqs[a])  
    for sh in range(0,128):
      icms.append(icm(freqs[0], shift))
      # shift Ci one char
      shift.append(shift.pop(0))
    keyshifts.append(icms.index(max(icms)))
  return keyshifts
    

def icm(x,y):
    lx = float(len(x))
    ly = float(len(y))
    return sum( map(lambda (a,b): (a/lx) * (b/ly), zip(x,y)) ) / lx*ly

def possible_keys(keyshifts):
  return map(lambda y: ''.join(map(lambda x: chr(x+y), keyshifts)),range(0,128))
    

    
s = file2String(cipher)
l = findKeyLength(s)
#simpleguess(l,' ',s)
keyshifts = ICMguess(l,s)
for key in possible_keys(keyshifts):
    print(key)
  
#print(coinc_idx(s))
