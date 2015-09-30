#!/usr/bin/env python

import getopt, sys

# barcoder -h
# barcoder [-r] -b 3[:ADSFDSAGAFDSKG] -b 1[:DSAGHGTFG] [-B BARCODE.txt] [INPUT.fa] [-s OUT.csv] > OUT.fa

__VERSION__="0.1.0"

BUILT_IN_BARCODES=[
    "wwyhwyyhmm",
    "whwmmhyhyy",
    "wwhhmwmmyw",
    "whyymmwmwm",
    "hwwmyhhmhw",
    "hmhyywhhym",
    "mmymwmwhhw",
    "myyhhmywyy",
    "hhyhwymmwy",
    "hymmywywhh",
    
    "ywwmhmhyyh",
    "yhmymhwwhy",
    "wmmhhywhyw",
    "hmmwhwmyyh",
    "myhhmmwwyh",
    "wwhhwwymym",
    "wwhhymmhhy",
    "wwywmmyhwh",
    "wwmmyhhymm",
    "whmymymyww",
    
    "hyhymyhwmm",
    "mmhwyywwmy",
    "ymwhmmhhww",
    "whwwhhyywm",
    "whwwmmwmyy",
    "whwmwyyhhw",
    "whhmhyhwyy",
    "whhyywwhwm",
    "wmwwywymmh",
    "wmmwwhmhwy",
    
    "hwyyhmmymy",
    "hmmyymwwym",
    "hmywmyhhyy",
    "mwyhwhhyhy",
    "mwmyhmwmwh",
    "myyhhyhhwm",
    "yywmwhymmy",
    "hhwhywhyhm",
    "whmmyyhyww",
    "wmhywhymyh",
]


def main(argv):
    '''Main program entry point'''
    
    # parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrb:B:s:S:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)
    
    # argument defaults
    inputFilenames = ["-"]
    barcodeMode = True
    positions=[]
    barcodes=[]
    barcodeFilename=None
    statsFilename=None
#     residuesFilename=None
    residueSeparator="__BC__"
    
    # process arguments
    if len(args) >= 1:
        inputFilenames = args
    for o, a in opts:
        if o == "-r":
            barcodeMode = False
        elif o in ("-b"):
            bc = a.split(":", 1)
            if len(bc) > 1 and len(bc[1]):
                barcodes.append(bc[1])
            try:
                positions.append(int(bc[0]))
            except ValueError:
                positions.append(0)
        elif o in ("-B"):
            barcodeFilename = a
#         elif o in ("-R"):
#             residuesFilename = a
        elif o in ("-s"):
            statsFilename = a
        elif o in ("-S"):
            residueSeparator = a
        else:
            print("Unknown option: %s" % o)
            usage()
            return 1
    # next argument
    
    # validate options
    if barcodeMode:
        for pos in positions:
            if pos < 1:
                print("Error: Positions need to be greater than 0 (found: %s)" % pos)
                usage()
                return 2
    else:
        pass
    
    # do work
    if barcodeMode:
        for inFile in inputFilenames:
            rc = barcode(inFile, positions, barcodes, barcodeFilename, residueSeparator)
            if rc != 0:
                return rc
        # next file
    else:
        rc = reconstruct(inputFilenames, positions, barcodes, barcodeFilename, statsFilename, residueSeparator)
        if rc != 0:
            return rc
        # next file
    return 0
# end main()

def barcode(inputFile, positions, barcodes, barcodeFilename, residueSeparator):
    '''Applies barcodes to the named inputfile'''
    
    # read barcodes if needed
    if barcodeFilename is not None:
        with open(barcodeFilename) as iFile:
            for line in iFile:
                if len(barcodes) >= len(positions):
                    break
                barcodes.append(line.rstrip())
            # next line
        # close iFile
    # endif barcodeFilename
    
    # use built in barcodes if needed
    if len(barcodes) < len(positions):
        barcodes.extend(BUILT_IN_BARCODES)
    
    # check enough barcodes are present
    if len(barcodes) < len(positions):
        print("Error: not enough barcodes were provided (or built in).  Please provide more")
        return 1
    
    # get input file handle
    rc = 0
    if inputFile == '-':
        iFile = sys.stdin
        rc = barcodeFile(sys.stdin, positions, barcodes, residueSeparator)
    else:
        with open(inputFile) as iFile:
            rc = barcodeFile(iFile, positions, barcodes, residueSeparator)
    
    return rc
# end barcode()

def barcodeFile(iFile, positions, barcodes, residueSeparator):
    '''Barcodes each sequence in the given file-like object'''
    
    sid = None
    seq = ""
    for line in iFile:
        line = line.rstrip()
        if line.startswith(">"):
            # complete last sequence
            if sid is not None:
                bcseq, residues = barcodeSequence(seq, positions, barcodes)
                print sid + residueSeparator + "".join(residues) + residueSeparator
                print bcseq
                
                seq = ""
            elif seq != "":
                print("Error: input file doesn't appear to be a FastA formatted file")
                return 1
            
            sid = line
        else:
            seq += line
        # endif
    # next line
    
    # complete final sequence
    if seq is not None:
        bcseq, residues = barcodeSequence(seq, positions, barcodes)
        print sid + residueSeparator + "".join(residues) + residueSeparator
        print bcseq
    
# end barcodeFile()

def barcodeSequence(seq, positions, barcodes):
    '''Barcodes a single sequence at specified positions'''
    result = []
    residues = []
        
    # do replacements
    lastpos = 0
    i = 0
    for pos in positions:
        result.append(seq[lastpos:pos-1])
        result.append(barcodes[i])
        residues.append(seq[pos-1:pos])
        lastpos = pos
        i+=1
    result.append(seq[lastpos:])
    
    # format results
    return ("".join(result), residues)
# end barcodeSequence

class BufferedReader():
    '''An iterable that allows peaking at next element'''
    
    def __init__(self, filename):
        self._filename = filename
        self._iterable = None #obj.__iter__()
        self._isEnd = False
        self._buffer = None
    
    def _checkOpen(self):
        if self._iterable is None:
            if self._filename == '-':
                self._iterable = sys.stdin
            else:
                self._iterable = open(self._filename)
    
    def __iter__(self):
        return self
    
    def next(self):
        self._checkOpen()
        if self._isEnd:
            raise StopIteration
        if self._buffer is not None:
            tmp = self._buffer
            self._buffer = None
            return tmp
        return self._iterable.next()
    
    def peek(self):
        '''Gives the next element without moving position'''
        if self._buffer is None:
            try:
                self._buffer = self.next()
            except StopIteration:
                self._isEnd = True
                return None
        return self._buffer
    
    def close(self):
        if self._iterable != sys.stdin:
            self._iterable.close()
# end BufferedReader()

def reconstruct(inputFilenames, positions, barcodes, barcodeFilename, statsFilename, residueSeparator):
    '''Removes barcodes and replaces residues'''
    
    if len(inputFilenames) < 1:
        return 3
    
    # make readers for each file (lazy opening)
    fileReaders = []
    for inFilename in inputFilenames:
        fileReaders.append(BufferedReader(inFilename))
    
    # count how many residues are in id (of first file)
    if len(positions) == 0:
        line = fileReaders[0].peek()
        if line is None:
            return 0
        if len(line) > 0 and line[0] != ">":
            print("Error: input file doesn't appear to be a FastA formatted file")
            return 1
        parts = line.split(residueSeparator, 2)
        if len(parts) > 1:
            positions = range(len(parts[1])) # make some fake positions (only count is used)

    # read barcodes if needed
    if barcodeFilename is not None:
        with open(barcodeFilename) as iFile:
            for line in iFile:
                if len(barcodes) >= len(positions):
                    break
                barcodes.append(line.rstrip())
            # next line
        # close iFile
    # endif barcodeFilename
    
    # open stats file
    statsFile = None
    if statsFilename is not None:
        statsFile = open(statsFilename, 'wb')
    
        # write header line 1
        statsFile.write("")
        statsFile.write(",Full,,")
        statsFile.write(",N-ter,,")
        for i in range(len(positions) -1):
            statsFile.write(",loop%s,," % (i+1))
        statsFile.write(",C-ter,,\n")
            
        # write header line 2
        statsFile.write("NAME")
        for _ in range(len(positions) + 2):
            statsFile.write(",length,hydropathy,charge")
        statsFile.write("\n")
    
    # use built in barcodes if needed
    if len(barcodes) < len(positions):
        barcodes.extend(BUILT_IN_BARCODES)
    
    # check enough barcodes are present
    if len(barcodes) < len(positions):
        print("Error: not enough barcodes were provided (or built in).  Please provide more")
        return 2

    # process the files
    for iFile in fileReaders:
        rc = 3
        try:
            # do reconstruction
            rc = reconstructFile(iFile, positions, barcodes, residueSeparator, statsFile)
        except:
            iFile.close()
            return 2
        
        if rc != 0:
            return rc
    
    # cleanup
    if statsFile is not None:
        statsFile.close()
    
# end reconstruct()


def reconstructFile(iFile, positions, barcodes, residueSeparator, statsFile=None):
    '''Removes barcodes and replaces residues for a file handle'''
    
    sid = None
    seq = ""
    for line in iFile:
        line = line.rstrip()
        if line.startswith(">"):
            # complete last sequence
            if sid is not None:
                seqid, rcseq, stats = reconstructSequence(sid, seq, positions, barcodes, residueSeparator)
                print seqid
                print rcseq
                if statsFile is not None:
                    statsFile.write("%s,%s\n" % (seqid, ",".join(stats)))
            elif seq != "":
                print("Error: input file doesn't appear to be a FastA formatted file")
                return 1
            
            sid = line
            seq = ""
        else:
            seq += line
        # endif
    # next line
    
    # complete final sequence
    if sid is not None:
        seqid, rcseq, stats = reconstructSequence(sid, seq, positions, barcodes, residueSeparator)
        print seqid
        print rcseq
        if statsFile is not None:
            statsFile.write("%s,%s\n" % (seqid, ",".join(stats)))
    elif seq != "":
        print("Error: input file doesn't appear to be a FastA formatted file")
        return 1

# end reconstructFile()

def _fixSplit(s, bc, bcp):
    '''Moves split point if a new point occurs before the current one'''
    if s < bcp:
        return s
    return s - len(bc) + 1

HYDROPATHY={
    "A": +1.8,
    "C": +2.5,
    "D": -3.5,
    "E": -3.5,
    "F": +2.8,
    "G": -0.4,
    "H": -3.2,
    "I": +4.5,
    "K": -3.9,
    "L": +3.8,
    "M": +1.9,
    "N": -3.5,
    "P": -1.6,
    "Q": -3.5,
    "R": -4.5,
    "S": -0.8,
    "T": -0.7,
    "V": +4.2,
    "W": -0.9,
    "Y": -1.3,
}

CHARGE={
    "D": -1,
    "E": -1,
    "K": +1,
    "R": +1,
#     "H": +0.1,
}

def _calcStats(seq):
    '''Returns stats for the given sequence'''
    
    hydropathy = 0.0
    charge = 0.0
    
    for r in seq:
        try:
            hydropathy += HYDROPATHY[r.upper()]
        except KeyError:
            pass
        try:
            charge += CHARGE[r.upper()]
        except KeyError:
            pass
    # next residue
    
    return (str(len(seq)), "%.1f" % hydropathy, "%.1f" % charge)
    

def reconstructSequence(sid, seq, positions, barcodes, residueSeparator):
    '''removes barcodes and replaces residues in a sequence'''
    
    # retrieve residues
    parts = sid.split(residueSeparator, 2)
    sidOut = parts[0]
    if len(parts) == 2:
        sidOut += parts[2]
    residues = []
    if len(parts) > 1:
        residues = list(parts[1])
    
    # make lowercase barcodes
    lcBarcodes = map(lambda s: s.lower(), barcodes)
    
    # replace barcodes
    seqOut = seq
    splits = []
    for i in range(len(positions)):
        bc = lcBarcodes[i]
        residue = "".join(residues[i:i+1])
        bcp = seqOut.find(bc)
        if bcp != -1:
            splits = map(lambda s: _fixSplit(s, bc, bcp), splits)
            splits.append(bcp)
        else:
            sys.stderr.write("Warning: barcode '%s' not found in sequence '%s'\n" % (bc, seq))
        seqOut = seqOut.replace(bc, residue, 1)
    
    # calculate stats
    splits.sort()
    lsp = 0
    stats = []
    stats.extend(_calcStats(seqOut))
    for sp in splits:
        stats.extend(_calcStats(seqOut[lsp:sp]))
        lsp = sp+1
    # next split 
    stats.extend(_calcStats(seqOut[lsp:]))
    
    
    return (sidOut, seqOut, stats)
# end reconstructSequence()


def usage(longMsg=False):
    print("usage: %s -b POS1[:BARCODE1] [-b POS2[:BARCODE2] [-b ...]] [-B BARCODE.txt]" % sys.argv[0])
    print("                [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] > OUTPUT.fa")
    print("       %s -r -b [POS1]:BARCODE1 [-b [POS2]:BARCODE2 [-b ...]] [-B BARCODE.txt]" % sys.argv[0])
    print("                [-s OUTPUT.csv] [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] > OUTPUT.fa")
    print("       %s -h | --help" % sys.argv[0])
    if longMsg is True:
        print("")
        print(" -h, --help        Print this help information")
        print(" -r                Operate in reconstruction mode (i.e. restoring residues)")
        print(" -b POS[:BARCODE]  Specify the POSition to replace with BARCODE")
        print("    POS            Residue index (1-based number) to replace in each sequence")
        print("    BARCODE        Barcode to use at this position.  Uses built-in (or see -B option)")
        print(" -B BARCODE.txt    Use file named BARCODE.txt to source barcodes from, one per line")
        print(" -s OUTPUT.csv     Produce (and store) summary statistics file named OUTPUT.csv")
        print(" -S SEPARATOR      String to enclose replaced residues when placed in FastA ID (Default: '__BC__')")
        print(" INPUT.fa          Input fasta sequences. '-' to read from standard input (Default)")
        print(" > OUTPUT.fa       Output fasta sequences are written to standard output.  Redirect to OUTPUT.fa")
    # end if long
    
    print("")
    print(" Version: %s" % __VERSION__)
# end usage()


if __name__=="__main__":
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
        usage(True)
        sys.exit(0)
    else:
        sys.exit(main(sys.argv[1:]))

## EOF ##
