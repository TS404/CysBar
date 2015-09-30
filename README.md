Readme for running cysbar.py locally
====================================
>Thomas M A Shafee, Andrew J Robinson, Nicole van der Weerden, Marilyn A Anderson

>Department of Biochemistry, La Trobe Institute for Molecular Science, La Trobe University, Melbourne, Australia  
>College of Science, Health and Engineering, La Trobe University, Melbourne, Australia  
>Life Sciences Computation Centre, Victorian Life Sciences Computation Initiative, Melbourne, Australia


Usage
-----
To barcode sequences:
```
cysbar.py -b POS1[:BARCODE1] [-b POS2[:BARCODE2] [-b ...]] [-B BARCODE.txt] [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] > OUTPUT.fa
```
To reconstruct sequences:
```
cysbar.py -r -b [POS1]:BARCODE1 [-b [POS2]:BARCODE2 [-b ...]] [-B BARCODE.txt] [-s OUTPUT.csv] [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] > OUTPUT.fa
```
Arguments:
```
-h, --help        Print this help information
-r                Operate in reconstruction mode (i.e. restoring residues)
-b POS[:BARCODE]  Specify the POSition to replace with BARCODE
   POS            Residue index (1-based number) to replace in each sequence
   BARCODE        Barcode to use at this position.  Uses built-in (or see -B option)
-B BARCODE.txt    Use file named BARCODE.txt to source barcodes from, one per line
-s OUTPUT.csv     Produce (and store) summary statistics file named OUTPUT.csv
-S SEPARATOR      String to enclose replaced residues when placed in FastA ID (Default: '__BC__')
INPUT.fa          Input fasta sequences. '-' to read from standard input (Default)
\>OUTPUT.fa         Output fasta sequences are written to standard output.  Redirect to OUTPUT.fa
```
