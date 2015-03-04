#!/bin/bash
#
#SBATCH --zodes=1
#SBATCH --mem=12000
#SBATCH --time=600


###-------------###
### User inputs ###
###-------------###

# Input file name
INPUT="example.fa"

# Define locations of conserved cysteine columns
C1=3
C2=6
C3=9
C4=12
C5=15
C6=18
C7=21
C8=24

# Define barcodes
BARCODE1=pmhmmwphmmhw
BARCODE2=mwhmmhwhhhmw
BARCODE3=hmhwhwmmhwmw
BARCODE4=wwpmhwppkmwh
BARCODE5=pphhwmphwmmh
BARCODE6=mwwhmhphpphw
BARCODE7=hwmpmhwpmmwh
BARCODE8=pmwhwwhhpwmm


###------------------###
### Barcoding script ###
###------------------###

# Clear zero C variables and remove unneeded barcodes
if [ $C2 == 0 ]; then unset C2; unset BARCODE2; fi
if [ $C3 == 0 ]; then unset C3; unset BARCODE3; fi
if [ $C4 == 0 ]; then unset C4; unset BARCODE4; fi
if [ $C5 == 0 ]; then unset C5; unset BARCODE5; fi
if [ $C6 == 0 ]; then unset C6; unset BARCODE6; fi
if [ $C7 == 0 ]; then unset C7; unset BARCODE7; fi
if [ $C8 == 0 ]; then unset C8; unset BARCODE8; fi

# Create empty column sequence files in case not all barcodes are present
touch column1.fa
touch column2.fa
touch column3.fa
touch column4.fa
touch column5.fa
touch column6.fa
touch column7.fa
touch column8.fa

# Save original columns for later re-integration
if [ -z $C1 ]; then echo empty column;
else awk '/^>/{print   }      /^[a-zA-Z-]/{print substr($0,'$C1',1)}' "$INPUT" >column1.fa
fi

if [ -z $C2 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C2',1)}' "$INPUT" >column2.fa
fi

if [ -z $C3 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C3',1)}' "$INPUT" >column3.fa
fi

if [ -z $C4 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C4',1)}' "$INPUT" >column4.fa
fi

if [ -z $C5 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C5',1)}' "$INPUT" >column5.fa
fi

if [ -z $C6 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C6',1)}' "$INPUT" >column6.fa
fi

if [ -z $C7 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C7',1)}' "$INPUT" >column7.fa
fi

if [ -z $C8 ]; then echo empty column;
else awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$C8',1)}' "$INPUT" >column8.fa
fi

# Fix empty C variables to be last highest C variable
if [ -z $C2 ]; then let C2=$C1; fi
if [ -z $C3 ]; then let C3=$C2; fi
if [ -z $C4 ]; then let C4=$C3; fi
if [ -z $C5 ]; then let C5=$C4; fi
if [ -z $C6 ]; then let C6=$C5; fi
if [ -z $C7 ]; then let C7=$C6; fi
if [ -z $C8 ]; then let C8=$C7; fi

# Copy >fastaname
# Copy first string up to Cysteine column 1
# Insert barcode
# etc. for each loop
awk '/^>/{print $0}\
/^[a-zA-Z-]/{print substr($0,1,'$C1'-1)"\
'$BARCODE1'"substr($0,'$C1'+1,'$C2'-'$C1'-1)"\
'$BARCODE2'"substr($0,'$C2'+1,'$C3'-'$C2'-1)"\
'$BARCODE3'"substr($0,'$C3'+1,'$C4'-'$C3'-1)"\
'$BARCODE4'"substr($0,'$C4'+1,'$C5'-'$C4'-1)"\
'$BARCODE5'"substr($0,'$C5'+1,'$C6'-'$C5'-1)"\
'$BARCODE6'"substr($0,'$C6'+1,'$C7'-'$C6'-1)"\
'$BARCODE7'"substr($0,'$C7'+1,'$C8'-'$C7'-1)"\
'$BARCODE8'"substr($0,'$C8'+1,1000)}'        \
"$INPUT" >BARCODED_"$INPUT"

exit 0
