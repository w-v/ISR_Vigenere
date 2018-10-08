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
    return l_coinc_idx.index(maximum)

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
  for a in range(0,l+1):
    subseq = cipher[a::l+1]
    print(subseq)
    freqs = [0] * 128
    for ch in subseq:
      freqs[ord(ch)]+=1
    key+=chr( ( freqs.index(max(freqs)) - ord(mf) )%128 )
    print(freqs)
  print(key)
      
s = file2String(cipher)
l = findKeyLength(s)
simpleguess(l,' ',s)

  
#print(coinc_idx(s))
