#!/usr/bin/env python

import getopt, sys, re

__VERSION__="1.0.1"
MATCHSIM = 0.85

# default values
# (so cysbar can be used standalone)
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

HYDROPATHY={
    "A": +1.8,
#     "C": +2.5,
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


def main(argv):
    '''Main program entry point'''
    
    # parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrb:B:s:S:v:")
    except getopt.GetoptError as err:
        # print help information and exit:
        sys.strerr.write("%s\n" %str(err))
        usage(outstream=sys.stderr)
        return 2
    
    # argument defaults
    inputFilenames = ["-"]
    barcodeMode = True
    positions=[]
    barcodes=[]
    barcodeFilename=None
    statsFilename=None
    statsValuesFilename=None
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
        elif o in ("-s"):
            statsFilename = a
        elif o in ("-S"):
            residueSeparator = a
        elif o in ("-v"):
            statsValuesFilename = a
        else:
            _writeError("Unknown option: %s\n" % o)
            usage(outstream=sys.stderr)
            return 1
    # next argument
    
    # validate options
    if barcodeMode:
        for pos in positions:
            if pos < 1:
                _writeError("Error: Positions need to be greater than 0 (found: %s)\n" % pos)
                usage(outstream=sys.stderr)
                return 2
    else:
        pass
    
    # fix order of positions (if necessary)
    positions.sort()
    
    # do work
    if barcodeMode:
        for inFile in inputFilenames:
            rc = barcode(inFile, positions, barcodes, barcodeFilename, residueSeparator)
            if rc != 0:
                return rc
        # next file
    else:
        rc = reconstruct(inputFilenames, positions, barcodes, barcodeFilename, statsFilename, residueSeparator, statsValuesFilename)
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
        _writeError("Error: not enough barcodes were provided (or built in).  Please provide more\n")
        return 1
    
    # get input file handle
    rc = 0
    if inputFile == '-':
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
    
    # check if we can seek (and cache if not)
    try:
        iFile.seek(0)
    except IOError:
        # cache input since its stdin and can't be seeked
        iFile = list(iFile)
    
    # check if barcodes match sequence
    bcMatch = False
    
    for bc in barcodes:
        bc = bc.lower()
        for line in iFile:
            line = line.rstrip()
            if line.startswith(">"):
                # complete last sequence
                if sid is not None:
                    if isMatched(seq.lower(), bc, MATCHSIM):
                        bcMatch = True
                        _writeError("ERROR: %s matches barcode '%s'\n" %(sid, bc))
                    
                    seq = ""
                elif seq != "":
                    _writeError("Error: input file doesn't appear to be a FastA formatted file\n")
                    return 1
                
                sid = line
            else:
                seq += line
            # endif
        # next line
        # complete final sequence
        if seq != "":
            if isMatched(seq, bc, MATCHSIM):
                bcMatch = True
                _writeError("ERROR: %s matches barcode '%s'\n" %(sid, bc))
    # next barcode
    if bcMatch:
        return 2
    
    # reset file to start
    sid = None
    seq = ""
    try:
        iFile.seek(0)
    except AttributeError: # list has no seek
        pass
    
    for line in iFile:
        line = line.rstrip()
        if line.startswith(">"):
            # complete last sequence
            if sid is not None:
                bcseq, residues = barcodeSequence(seq, positions, barcodes)
                _writeOutput(sid + residueSeparator + "".join(residues) + residueSeparator)
                _writeOutput(bcseq)
                
                seq = ""
            elif seq != "":
                _writeError("Error: input file doesn't appear to be a FastA formatted file\n")
                return 1
            
            sid = line
        else:
            seq += line
        # endif
    # next line
    
    # complete final sequence
    if seq != "":
        bcseq, residues = barcodeSequence(seq, positions, barcodes)
        _writeOutput(sid + residueSeparator + "".join(residues) + residueSeparator)
        _writeOutput(bcseq)
        
    return 0
# end barcodeFile()

def barcodeSequence(seq, positions, barcodes):
    '''
    Barcodes a single sequence at specified positions.
    
    Positions list must be in order from lowest to highest
    '''
    result = []
    residues = []
        
    # do replacements
    lastpos = 0
    i = 0
    for pos in positions:
        
        # enforce position ordering
        if lastpos >= pos:
            return ("",[])
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
        self._iterable = None
        self._isEnd = False
        self._buffer = None
    
    def _checkOpen(self):
        '''Safely open the stream (if needed)'''
        if self._iterable is None:
            if self._filename == '-':
                self._iterable = sys.stdin
            else:
                self._iterable = open(self._filename)
    
    def __iter__(self):
        '''Get (self) as iterable'''
        return self
    
    def next(self):
        '''Next method to allow this class to be a python iterable'''
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
        '''Closes the underlying interator stream (if not stdin)'''
        if self._iterable != sys.stdin:
            self._iterable.close()
# end BufferedReader()

def reconstruct(inputFilenames, positions, barcodes, barcodeFilename, statsFilename, residueSeparator, statsValuesFilename):
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
            _writeError("Error: input file doesn't appear to be a FastA formatted file\n")
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
    
    # read stats values if needed
    if statsValuesFilename is not None:
        if not _loadHydroChargeFile(statsValuesFilename):
            return 4
                
    # endif statsValuesFilename
    
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
        _writeError("Error: not enough barcodes were provided (or built in).  Please provide more\n")
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
    
    return 0
# end reconstruct()


def _loadHydroChargeFile(filename):
    '''Updates the Hydropathy and Charge values based on the contents of CSV file'''
    
    with open(filename) as iFile:
        HYDROPATHY.clear()
        CHARGE.clear()
        
        # read each line
        for line in iFile:
            cols = line.rstrip().split(",")
            
            # ignore empty and comment lines
            if not line.startswith("#") and len(cols) != 0:
                if len(cols) in (2,3) and len(cols[0]) == 1:
                    cols[1] = cols[1].strip()
                    if cols[1] != "":
                        HYDROPATHY[cols[0].upper()] = float(cols[1])
                    if len(cols) == 3:
                        cols[2] = cols[2].strip()
                        if cols[2] != "":
                            CHARGE[cols[0].upper()] = float(cols[2].strip())
                else:
                    _writeError("Error: Unable to read Hydropathy and Charge values file.\n")
                    _writeError("       Expected CSV format no header and columns Residue, Hydropathy and Charge.\n")
                    return False
    return True

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
                _writeOutput(seqid)
                _writeOutput(rcseq)
                if statsFile is not None:
                    statsFile.write("%s,%s\n" % (seqid, ",".join(stats)))
            elif seq != "":
                _writeError("Error: input file doesn't appear to be a FastA formatted file\n")
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
        _writeOutput(seqid)
        _writeOutput(rcseq)
        if statsFile is not None:
            statsFile.write("%s,%s\n" % (seqid, ",".join(stats)))
    elif seq != "":
        _writeError("Error: input file doesn't appear to be a FastA formatted file\n")
        return 1
    return 0

# end reconstructFile()

def _fixSplit(s, bc, bcp):
    '''Moves split point if a new point occurs before the current one'''
    if s < bcp:
        return s
    return s - len(bc) + 1

def _calcStats(seq):
    '''Returns stats for the given sequence'''
    
    hydropathy = 0.0
    charge = 0.0
    
    # remove all non-letters
    seq = re.sub(r'[^A-Z]', '', seq.upper())
    hyLength = 0
    
    for r in seq:
        try:
            hydropathy += HYDROPATHY[r.upper()]
            hyLength += 1
        except KeyError:
            pass
        try:
            charge += CHARGE[r.upper()]
        except KeyError:
            pass
    # next residue
    
    length = len(seq)
    
    if hyLength == 0:
        hh = "1E-100"
        cc = "1E-100"
    else:
        hh = "%.5f" % (hydropathy / hyLength)
        cc = "%.1f" % charge
    
    return (str(length), hh, cc)
    

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
            _writeError("Warning: barcode '%s' not found in sequence '%s'\n" % (bc, seq))
        seqOut = seqOut.replace(bc, residue, 1)
    
    # calculate stats
    splits.sort()
    lsp = 0
    stats = []
    statsC = _calcStats(seqOut)
    fullSeq = ""
    for sp in splits:
        fullSeq += seqOut[lsp:sp]
        stats.extend(_calcStats(seqOut[lsp:sp]))
        lsp = sp+1
    # next split 
    fullSeq += seqOut[lsp:]
    stats.extend(_calcStats(seqOut[lsp:]))
    statsNC = _calcStats(fullSeq)
    
    outStats = [statsC[0], statsNC[1], statsC[2]]
    outStats.extend(stats)
    
    return (sidOut, seqOut, outStats)
# end reconstructSequence()


def usage(longMsg=False, outstream=sys.stdout):
    outstream.write("usage: %s -b POS1[:BARCODE1] [-b POS2[:BARCODE2] [-b ...]] [-B BARCODE.txt]\n" % sys.argv[0])
    outstream.write("                [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] > OUTPUT.fa\n")
    outstream.write("       %s -r [-b [POS1]:BARCODE1] [-b [POS2]:BARCODE2 [-b ...]] [-B BARCODE.txt]\n" % sys.argv[0])
    outstream.write("                [-s OUTPUT.csv] [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] ")
    outstream.write("                [-v HYDROCHARGE.csv] > OUTPUT.fa\n")
    outstream.write("       %s -h | --help\n" % sys.argv[0])
    if longMsg is True:
        outstream.write("\n")
        outstream.write(" -h, --help          Print this help information\n")
        outstream.write(" -r                  Operate in reconstruction mode (i.e. restoring residues)\n")
        outstream.write(" -b POS[:BARCODE]    Specify the POSition to replace with BARCODE\n")
        outstream.write("    POS              Residue index (1-based number) to replace in each sequence\n")
        outstream.write("    BARCODE          Custom barcode to use at this position.  Uses built-in (or see -B option)\n")
        outstream.write(" -B BARCODE.txt      Use file named BARCODE.txt to source barcodes from, one per line\n")
        outstream.write(" -s OUTPUT.csv       Produce (and store) summary statistics file named OUTPUT.csv\n")
        outstream.write(" -S SEPARATOR        String to enclose replaced residues in FastA ID (Default: '__BC__')\n")
        outstream.write(" -v HYDROCHARGE.csv  CSV file containing new Hydropathy and Charge values for each residue.\n")
        outstream.write("                     Contains Residue, Hydropathy and Charge columns (no headers).\n")
        outstream.write(" INPUT.fa            Input FastA file. (default: standard input)\n")
        outstream.write(" > OUTPUT.fa         Output FastA file. (default: standard output)\n")
    # end if long
    
    outstream.write("\n")
    outstream.write(" Version: %s\n" % __VERSION__)
# end usage()


#### SUPPORT ####

class BarcodeMatch(Exception):
    pass
 
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
            goodAlign(seq, bc, 0, -pen, pen, OVERLAP)[0]
            
        
        # match with equal start, seq start or barcode past end
        for seqpos in range(seqlen):
            goodAlign(seq, bc, seqpos, 0, OVERLAP)[0]
        
    except BarcodeMatch:
        return True
    return False
# end isMatched
    

def goodAlign(seq, bc, seqpos, bcpos, pen=0, OVERLAP = 8):
    '''Tree-recusively checks for an alignment of bc in seq allowing for mismatchs and indels'''
    
    if (seqpos,bcpos) in _CACHE:
        return _CACHE[(seqpos,bcpos)]
    
    # check if this residue aligns
    score = 0
    try:
        if seq[seqpos] == bc[bcpos]:
            score = 1
    except IndexError:
        _CACHE[(seqpos,bcpos)] = (0, "", "", "")
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
    
    if score[0] >= OVERLAP:
        raise BarcodeMatch
    
    return score
# end goodAlign

def _writeError(error):
    '''Writes an error to stderr'''
    sys.stderr.write(error)

def _writeOutput(output):
    '''Writes output to stdout'''
    print output



#### main entry point ####

if __name__=="__main__":
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
        usage(True)
        sys.exit(0)
    else:
        sys.exit(main(sys.argv[1:]))

## EOF ##