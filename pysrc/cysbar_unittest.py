'''
Created on 25 Nov 2015

@author: arobinson
'''
import unittest
import cysbar


#############
## SUPPORT ##
#############

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
    ]

ERRORS = []
OUTPUT = []
def _captureError(error):
    ERRORS.append(error)
def _captureOutput(output):
    OUTPUT.append(output)

residueSeparator="__BC__"


###########
## TESTS ##
###########

class TestBarcodeSequence(unittest.TestCase):
    '''Tests barcodeSequence() function'''

    def testBarcode1(self):
        sequence = "RDESQSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-"
        positions = [5]
        barcodes = BUILT_IN_BARCODES[:1]
        
        bcseq, residues = cysbar.barcodeSequence(sequence, positions, barcodes)
        
        self.assertEqual(bcseq, "RDESwwyhwyyhmmSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")
        self.assertEqual(residues, ['Q'])

    def testBarcode2(self):
        sequence = "RDESQSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-"
        positions = [5, 10]
        barcodes = BUILT_IN_BARCODES[:2]
        
        bcseq, residues = cysbar.barcodeSequence(sequence, positions, barcodes)
        
        self.assertEqual(bcseq, "RDESwwyhwyyhmmSHKFwhwmmhyhyyGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")
        self.assertEqual(residues, ['Q','K'])

    def testBarcode2reverse(self):
        sequence = "RDESQSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-"
        positions = [10, 5]
        barcodes = BUILT_IN_BARCODES[:2]
        
        bcseq, residues = cysbar.barcodeSequence(sequence, positions, barcodes)
        
        self.assertEqual(bcseq, "")
        self.assertEqual(residues, [])



class TestBarcode(unittest.TestCase):
    '''
    Tests barcode() function
    
    barcode(inputFile, positions, barcodes, barcodeFilename, residueSeparator)
    '''
    
    def testBarcodeParams(self):
        del ERRORS[:]
        del OUTPUT[:]
        cysbar._writeError = _captureError
        cysbar._writeOutput = _captureOutput
        positions = [5]
        barcodes = BUILT_IN_BARCODES[:1]
        rc = cysbar.barcode("../data/test/seq1.fa", positions, barcodes, None, residueSeparator)
        self.assertEqual(rc, 0)
        self.assertEqual(len(OUTPUT), 2)
        self.assertEqual(OUTPUT[0], ">seq1__BC__Q__BC__")
        self.assertEqual(OUTPUT[1], "RDESwwyhwyyhmmSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")
    
    def testBarcodeFile(self):
        del ERRORS[:]
        del OUTPUT[:]
        cysbar._writeError = _captureError
        cysbar._writeOutput = _captureOutput
        positions = [5]
        barcodes = []
        rc = cysbar.barcode("../data/test/seq1.fa", positions, barcodes, "../data/test/barcodes2.txt", residueSeparator)
        self.assertEqual(rc, 0)
        self.assertEqual(len(OUTPUT), 2)
        self.assertEqual(OUTPUT[0], ">seq1__BC__Q__BC__")
        self.assertEqual(OUTPUT[1], "RDESabc123SHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")


class TestReconstruct(unittest.TestCase):
    '''
    Tests reconstruct() function
    
    reconstruct(inputFilenames, positions, barcodes, barcodeFilename, statsFilename, residueSeparator)
    '''
    
    def testBarcodeParams(self):
        del ERRORS[:]
        del OUTPUT[:]
        cysbar._writeError = _captureError
        cysbar._writeOutput = _captureOutput
        positions = [5]
        barcodes = BUILT_IN_BARCODES[:1]
        rc = cysbar.reconstruct(["../data/test/seq1_pos5wwyhwyyhmm.fa"], positions, barcodes, None, None, residueSeparator, None)
        self.assertEqual(rc, 0)
        self.assertEqual(len(OUTPUT), 2)
        self.assertEqual(OUTPUT[0], ">seq1")
        self.assertEqual(OUTPUT[1], "RDESQSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")
    
    def testBarcodeFile(self):
        del ERRORS[:]
        del OUTPUT[:]
        cysbar._writeError = _captureError
        cysbar._writeOutput = _captureOutput
        positions = [5]
        barcodes = []
        rc = cysbar.reconstruct(["../data/test/seq1_pos5abc123.fa"], positions, barcodes, "../data/test/barcodes2.txt", None, residueSeparator, None)
        self.assertEqual(rc, 0)
        self.assertEqual(len(OUTPUT), 2)
        self.assertEqual(OUTPUT[0], ">seq1")
        self.assertEqual(OUTPUT[1], "RDESQSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")


class TestBufferedReader(unittest.TestCase):
    '''Tests BufferedReader class'''
    
    def testConstruct(self):
        r = cysbar.BufferedReader("../data/test/line1.txt")
    
    def testConstructNonExistent(self):
        r = cysbar.BufferedReader("../data/test/notexist.txt")
        self.assertRaises(IOError, r.next)
    
    def testPeekEmpty(self):
        r = cysbar.BufferedReader("../data/test/empty.txt")
        self.assertIsNone(r.peek())
        
    def testPeekLine1(self):
        r = cysbar.BufferedReader("../data/test/line1.txt")
        self.assertEqual(r.peek(), "Hello")
    
    def testNext1(self):
        r = cysbar.BufferedReader("../data/test/seq1.fa")
        self.assertEqual(r.next(), ">seq1\n")
    
    def testNextPastEnd(self):
        r = cysbar.BufferedReader("../data/test/seq1.fa")
        r.next()
        r.next()
        self.assertRaises(StopIteration, r.next)
        
    def testPeekLine2(self):
        r = cysbar.BufferedReader("../data/test/seq1.fa")
        r.next()
        self.assertEqual(r.peek(), "RDESQSHKFKGTIR---XSNRDCESQSHKFKGTCIR---XSNCASVCXS-E-GF--NGGHCRG--RRCYCTAK-")
        
    def testForLoop1(self):
        r = cysbar.BufferedReader("../data/test/line1.txt")
        c = 0
        for _ in r:
            c += 1
        self.assertEqual(c, 1)
        
    def testForLoop0(self):
        r = cysbar.BufferedReader("../data/test/empty.txt")
        c = 0
        for _ in r:
            c += 1
        self.assertEqual(c, 0)
        
    def testForLoop2a(self):
        r = cysbar.BufferedReader("../data/test/seq1.fa")
        c = 0
        for _ in r:
            c += 1
        self.assertEqual(c, 2)
        
    def testForLoop2b(self):
        r = cysbar.BufferedReader("../data/test/seq1b.fa")
        c = 0
        for _ in r:
            c += 1
        self.assertEqual(c, 2)
        
class TestCalcStats(unittest.TestCase):
    '''Tests _calcStats function'''
    
    def test1(self):
        l, h, c = cysbar._calcStats("RDESQ")
        self.assertEqual("5", l)
        self.assertEqual("-3.16000", h)
        self.assertEqual("-1.0", c)
    
    def testNoHydro(self):
        l, h, c = cysbar._calcStats("CCC")
        self.assertEqual("3", l)
        self.assertEqual("1E-100", h)
        self.assertEqual("1E-100", c)
    
    def testZeroHydro(self):
        l, h, c = cysbar._calcStats("RIRI")
        self.assertEqual("4", l)
        self.assertEqual("0.00000", h)
        self.assertEqual("2.0", c)
    
    def testNoCharge(self):
        l, h, c = cysbar._calcStats("MMM")
        self.assertEqual("3", l)
        self.assertEqual("1.90000", h)
        self.assertEqual("0.0", c)
    
    def testZeroCharge(self):
        l, h, c = cysbar._calcStats("DKDK")
        self.assertEqual("4", l)
        self.assertEqual("-3.70000", h)
        self.assertEqual("0.0", c)
        
class TestCalcStatsCustom(unittest.TestCase):
    '''Tests _calcStats function'''
        
    def testCustomTablePresent(self):
        cysbar._loadHydroChargeFile("../data/test/hydropathy_charge.csv")
        l, h, c = cysbar._calcStats("AY")
        self.assertEqual("2", l)
        self.assertEqual("-1.50000", h)
        self.assertEqual("7.0", c)
        
    def testCustomTableAbsent(self):
        cysbar._loadHydroChargeFile("../data/test/hydropathy_charge.csv")
        l, h, c = cysbar._calcStats("AD")
        self.assertEqual("2", l)
        self.assertEqual("1.00000", h)
        self.assertEqual("5.0", c)
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    