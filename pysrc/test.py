'''
Created on 23 Sep 2015

@author: arobinson
'''
import sys


# t = list(sys.stdin)
# print t

# sys.stdin.seek(0)

[].seek(0)



# ## check see on a file
# with open("INSTALL.txt") as f:
#     line = f.readline()
#     print "Line1 %s" % line.rstrip()
#     f.seek(0)
#     line = f.readline()
#     print "Line2 %s" % line.rstrip()
# 
# 
# ## check seek on std input
# line = sys.stdin.readline()
# print "Line3 %s" % line
# sys.stdin.seek(0)





## compare sequence to

class BarcodeMatch(Exception):
    pass

#OVERLAP=8
 
_CACHE={}

def isMatched(seq, bc, matchSim = 0.85):
    '''Checks if barcode is in seq significantly'''
    
    
    seqlen = len(seq)
    bclen = len(bc)
    _CACHE.clear()
    
    OVERLAP = int(min(seqlen, bclen) * matchSim)
    
    
    try:
        # match with barcode at start
        for pen in range(OVERLAP-bclen,0):
#             print "Trying: %s %s %s" % (0, -pen, pen)
#             print "Score: %s" % 
            goodAlign(seq, bc, 0, -pen, pen, OVERLAP)[0]
            
        
        # match with equal start, seq start or barcode past end
        for seqpos in range(seqlen):
#             print "Trying: %s %s %s" % (seqpos, 0,0)
#             print "Score: %s" % 
            goodAlign(seq, bc, seqpos, 0, OVERLAP)[0]
        
    except BarcodeMatch:
        return True
    return False
# end isMatched
    

def goodAlign(seq, bc, seqpos, bcpos, pen=0, OVERLAP = 8):
    if (seqpos,bcpos) in _CACHE:
        return _CACHE[(seqpos,bcpos)]
    
    # check if this residue aligns
    score = 0
    try:
        if seq[seqpos] == bc[bcpos]:
            score = 1
    except IndexError:
        _CACHE[(seqpos,bcpos)] = (0, "", "", "")
#         print "[%s, %s]: %s" % (seqpos, bcpos, 0)
        return (0, "", "", "")
    
    # compute rest of alignment
    m1 = goodAlign(seq, bc, seqpos+1, bcpos+1, OVERLAP)  # match (or mismatch)
    m2 = goodAlign(seq, bc, seqpos, bcpos+1, OVERLAP)    # barcode insertion
    m3 = goodAlign(seq, bc, seqpos+1, bcpos, OVERLAP)    # sequence insertion
    
    ms = max(m1[0]+score, m2[0], m3[0])
    
    if ms == m1[0]+score:
        score = (m1[0]+score, seq[seqpos] + m1[1], "|" + m1[2], bc[bcpos] + m1[3])
    elif ms == m2[0]:
        score = (m2[0]+score, "-"+ m2[1], " " + m2[2], bc[bcpos] + m2[3])
    else:
        score = (m3[0]+score, seq[seqpos] + m3[1], " " + m3[2], "-" + m3[3])
 
    # cache the score
    _CACHE[(seqpos,bcpos)] = score
    
#     print "[%s, %s]: %s" % (seqpos, bcpos, score)
    
    if score[0] >= OVERLAP:
#         print score[1]
#         print score[2]
#         print score[3]
        raise BarcodeMatch
    
    return score
# end goodAlign

BC = "ABCDEFGHI"

SEQS=[
      "DIEIJFKDSLWEISVLKJZFSDFGLKJSGDOIWERSLKDFJLSKFD",
      "IFGJFDSGVLKJSGDLKJABCDEFDFDFDFDFDDFDFFGHIFLKEWEIJFDLSKJSDLFK",
      "AAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "DSFJRIFGJFDAKBKCKDKEKFKGKHKIKJKKLKMKNKOKPKSGKJDSVKJREFGSDF",
      "ABDEFGHIJKLMDSFSDJFKEWQIJSAKJSAVDSAF",
      ]

for seq in SEQS:
    print "%s: %s" % (seq, isMatched(seq, BC))

