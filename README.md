Readme for running cysbar.py locally
====================================
>Thomas M A Shafee, Andrew J Robinson, Nicole van der Weerden, Marilyn A Anderson

>Department of Biochemistry, La Trobe Institute for Molecular Science, La Trobe University, Melbourne, Australia  
>College of Science, Health and Engineering, La Trobe University, Melbourne, Australia  
>Life Sciences Computation Centre, Victorian Life Sciences Computation Initiative, Melbourne, Australia


Usage
-----

```in
Barcoding function:
cysbar.py -b POS1[:BARCODE1] [-b POS2[:BARCODE2] [-b ...]] [-B BARCODE.txt] [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] >OUTPUT.fa

Reconstructing function:
cysbar.py -r -b [POS1:][BARCODE1] [-b [POS2:][BARCODE2] [-b ...]] [-B BARCODE.txt] [-s OUTPUT.csv] [-S SEPARATOR] [INPUT.fa [INPUT2.fa ...]] >OUTPUT.fa

Arguments:
-h, --help        Print this help information
-r                Operate in reconstruction mode (i.e. restoring residues)
-b POS[:BARCODE]  Specify the POSition to replace with BARCODE
   POS            Residue index (1-based number) to replace in each sequence
   BARCODE        Custom barcode to use at this position (or see -B option)
-B BARCODE.txt    Use file named BARCODE.txt to source barcodes from, one per line
-S SEPARATOR      String to enclose replaced residues when placed in FastA ID (Default: '__BC__')
INPUT.fa          Input fasta file (default = standard input)
>OUTPUT.fa        Output fasta file (default = standard output)
```

Manual
------

### 1 Readme introduction

This readme describes in detail how to use the python script `cysbar.py` locally and how to use the data analysing excel spreadsheet `loopproperties.xlsx`. For simple online use of the scripts a webtool is available at [cysbar.science.latrobe.edu.au](http://cysbar.science.latrobe.edu.au).


### 2 Python

The script is in the python programming language and runs on linux, or mac machine. Windows users need to install python. A short tutorial of the necessary basics to run pyton scripts is here:  
[www.python.org](https://www.python.org/about/gettingstarted/)  
The script is annotated and can be opened by any text editor to read and edit.

Both barcoding and reconstructing functions need the user to define some basic parameters (arguments). These are entered after `cysbar.py` with `-x` commands.

### 3 Using the barcoding function

The input alignment is barcoded using `cysbar.py`, which replaces columns of a fasta file (specified by `-b` arguments). Removed residues are stored in the fasta ID between `__BC__` separators. Custom barcodes can be used either by providing a list of sequences (`-B` argument) or by defining a custom barcode to be used at a specific position (`-b POS:BARCODE` argument).

Command for barcoding:
```
cysbar.py -b POS1 -b POS2 ...
```

Optional arguments:
```
-b POS:BARCODE    Use a custom barcode at this position
-B BARCODE.txt    Use file named BARCODE.txt to source barcodes from, one per line
-S SEPARATOR      String to enclose replaced residues when placed in FastA ID (Default: '__BC__')
INPUT.fa          Input fasta file (default = standard input)
>OUTPUT.fa        Output fasta file (default = standard output)
```

Example:
```
cysbar.py -b 11 -b 22 -b 28 -b 32 -b 43 -b 50 -b 52 -b 56 example.fa >BARCODED_example.fa
```
The above command will barcode the 11th, 29th... etc. columns of the `example.fa` alignment using the deafult barcode set, creating an output alignment called `BARCODED_example.fa`. The `BARCODED_example.fa` file can then be re-aligned by any standard alignment program (e.g. ClustalΩ, Probcons, Muscle).

*Notes*:  
When several sub-group alignments need to be combined into a single alignment barcoded alignment, the individual sub-group alignments should be barcoded independently with `cysbar.py` (as in the example figures used in the manuscript).
The barcoded alignments should then be concatenated into a single alignment file. This single combined alignment can be re-aligned with any standard alignment program. The reconstruction function can then be run on the re-aligned, combined alignment.

### 4 Using the reconstructer function

Once the barcoded alignment has been re-aligned by an appropriate program, `cysbar.py -r` replaces the barcoded columns of a fasta file with the original columns that were removed and saved in the fasta ID by barcoding function. Additionally, it can provide summary file of the length, hydrophobicity and charge of each inter-cysteine region (`-s` argument).

Command for reconstructing:
```
cysbar.py -r 
```
Optional arguments:
```
-s OUTPUT.csv     Produce (and save) summary statistics file named OUTPUT.csv
-b POS:BARCODE    Define the custom barcode used at this position
-B BARCODE.txt    Use file named BARCODE.txt to source used barcodes from, one per line
-S SEPARATOR      String that was used to enclose replaced residues in the FastA ID (Default: '__BC__')
INPUT.fa          Input fasta file (default = standard input)
>OUTPUT.fa        Output fasta file (default = standard output)
```

Example:
```
cysbar.py -r -s stats.csv example2.fa >FINAL.fa
```
The above command will restore the original sequences of the `example2.fa` alignment, creating an output alignment called `FINAL.fa` and a summary of statistics called `stats.csv`.

*Notes*:  
If the default barcodes was used, `-b` arguments are unnecessary since the script will search for the default barcode sequences. If custom barcode sequences were used, the same sequences must be definied in the `cysbar.py -r` command. For calculating loop properties, all cysteines are assumed to be oxidised (i.e. involved in disulphide bridges).


### 5 Using loopproperties.xlsx

If `cysbar.py -r` has been commanded to generate a statistics summary csv file (`-s`argument), the data from this can be copy-pasted into `loopproperties.xlsx` which will provide summary graphs. To use it follow these steps:

1. In Excel, open both the stastistics csv file and `loopproperties.xlsx`
2. Copy the whole spreadsheet of the statistics csv file
3. Paste the copied contents into the first worksheet page of `loopproperties.xlsx`
4. The subsequent worksheets of `loopproperties.xlsx` give the following information:  
 a. Length – amino acid length  
 b. Hydropathy – Doolittle index of hydrophobicity  
 c. Charge – net coulomb charge  
 d. Figures – a summary of bar charts and histograms from the other sheets  

*Notes*:  
This spreadcheet only functions for a maximum of 8 barcoded columns. Parameters with no data (e.g. the charge of a loop with length zero) are marked with 1E-100 to distinguish from true zero values (e.g. the charge of a neutral loop). These 1E-100 values are ignored when generating the subsequent charts.
