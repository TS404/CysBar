#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --mem=120000
#SBATCH --time=6000

###-------------###
### User inputs ###
###-------------###

# Input file name
INPUT2="newalign.fa"

# Define barcodes
BARCODE1=pmhmmwphmmhw
BARCODE2=mwhmmhwhhhmw
BARCODE3=hmhwhwmmhwmw
BARCODE4=wwpmhwppkmwh
BARCODE5=pphhwmphwmmh
BARCODE6=mwwhmhphpphw
BARCODE7=hwmpmhwpmmwh
BARCODE8=pmwhwwhhpwmm

###------------------------###
### Sequence reconstructer ###
###------------------------###

# Find the new locations of the barcode columns (from from sequence in fasta file)
B1=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE1"|awk -F : '{print $1}')
B2=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE2"|awk -F : '{print $1}')
B3=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE3"|awk -F : '{print $1}')
B4=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE4"|awk -F : '{print $1}')
B5=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE5"|awk -F : '{print $1}')
B6=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE6"|awk -F : '{print $1}')
B7=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE7"|awk -F : '{print $1}')
B8=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE8"|awk -F : '{print $1}')
 
# Find the N-terminal sequence
awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,1,'$B1')}' "$INPUT2"                 >Nter.fa

# Create empty loop sequence files in case not all barcodes are present
touch Nter.fa
touch loop1.fa
touch loop2.fa
touch loop3.fa
touch loop4.fa
touch loop5.fa
touch loop6.fa
touch loop7.fa
touch C-ter.fa

# Find the inter-loop regions if the barcodes exist and make loop sequence files
if [ -z "$B2" ]
then
	B1=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE1"|awk -F : '{print $1}')
	awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B1'+13,1000)}' "$INPUT2"           >Cter.fa
else
	B2=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE2"|awk -F : '{print $1}')
	awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B1'+13,'$B2'-'$B1'-12)}' "$INPUT2" >loop1.fa
	if [ -z "$B3" ]
	then
		B2=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE2"|awk -F : '{print $1}')
		awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B2'+13,1000)}' "$INPUT2"           >Cter.fa
	else
		B3=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE3"|awk -F : '{print $1}')
		awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B2'+13,'$B3'-'$B2'-12)}' "$INPUT2" >loop2.fa
		if [ -z "$B4" ]
		then
			B3=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE3"|awk -F : '{print $1}')
			awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B3'+13,1000)}' "$INPUT2"           >Cter.fa
		else
			B4=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE4"|awk -F : '{print $1}')
			awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B3'+13,'$B4'-'$B3'-12)}' "$INPUT2" >loop3.fa
			if [ -z "$B5" ]
			then
				B4=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE4"|awk -F : '{print $1}')
				awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B4'+13,1000)}' "$INPUT2"           >Cter.fa
			else
				B5=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE5"|awk -F : '{print $1}')
				awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B4'+13,'$B5'-'$B4'-12)}' "$INPUT2" >loop4.fa
				if [ -z "$B6" ]
				then
					B5=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE5"|awk -F : '{print $1}')
					awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B5'+13,1000)}' "$INPUT2"           >Cter.fa
				else
					B6=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE6"|awk -F : '{print $1}')
					awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B5'+13,'$B6'-'$B5'-12)}' "$INPUT2" >loop5.fa
					if [ -z "$B7" ]
					then
						B6=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE6"|awk -F : '{print $1}')
						awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B6'+13,1000)}' "$INPUT2"           >Cter.fa
					else
						B7=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE7"|awk -F : '{print $1}')
						awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B6'+13,'$B7'-'$B6'-12)}' "$INPUT2" >loop6.fa
						if [ -z "$B8" ]
						then 
							B7=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE7"|awk -F : '{print $1}')
							awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B7'+13,1000)}' "$INPUT2"           >Cter.fa
						else
							B8=$(head -n2 "$INPUT2"|tail -n1|grep -o -b "$BARCODE8"|awk -F : '{print $1}')
							awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B7'+13,'$B8'-'$B7'-12)}' "$INPUT2" >loop7.fa
							awk '/^>/{print ""}      /^[a-zA-Z-]/{print substr($0,'$B8'+13,1000)}' "$INPUT2"           >Cter.fa
						fi
					fi
				fi
			fi
		fi
	fi
fi

# paste the loops back inbetween the original columns that were removed for barcoding
paste -d @ \
Nter.fa  column1.fa \
loop1.fa column2.fa \
loop2.fa column3.fa \
loop3.fa column4.fa \
loop4.fa column5.fa \
loop5.fa column6.fa \
loop6.fa column7.fa \
loop7.fa column8.fa \
Cter.fa             |\
sed s/@//g          >FINAL_ALIGNMENT.fa


#-------------#
# Data values #
#-------------#

# Hydropathy values
VAR1=hydropathy
A=" +1.8"
C=" +2.5"
D=" -3.5"
E=" -3.5"
F=" +2.8"
G=" -0.4"
H=" -3.2"
I=" +4.5"
K=" -3.9"
L=" +3.8"
M=" +1.9"
N=" -3.5"
P=" -1.6"
Q=" -3.5"
R=" -4.5"
S=" -0.8"
T=" -0.7"
V=" +4.2"
W=" -0.9"
Y=" -1.3"

# Charge at pH7.4
VAR2=charge
D3=" -1"
E3=" -1"
K3=" +1"
R3=" +1"
# H3=" +0.1"

#----------------#
# File formatter #
#----------------#

# Create column headers for final .csv
echo ,\
full ,,,\
N-ter,,,\
loop1,,,\
loop2,,,\
loop3,,,\
loop4,,,\
loop5,,,\
loop6,,,\
loop7,,,\
C-ter,,,>header.tmp

echo \
NAME,\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2",\
length,"$VAR1","$VAR2", >>header.tmp

# Name column
# --------------
# Look only at lines with names in them,
# remove >s
# remove empty lines
# remove ^M returns
awk '/^>/{print}/^[a-zA-Z-]/{print $2}' FINAL_ALIGNMENT.fa |\
sed s/">"//g                                            |\
sed '/^$/d'                                             |\
sed 's/\r//g'                                           > names.tmp

#---------------------#
# Property calculator #
#---------------------#

# Define loop 0 as full sequence, Nter as loop 8, C-ter as loop 9
cp FINAL_ALIGNMENT.fa loop0.fa
cp Nter.fa            loop8.fa
cp Cter.fa            loop9.fa

# Do the following analysis for the full sequence (loop0) and each defined loop 1 to 7
for i in {0..9}
do
INPUTLOOP=loop"$i".fa

	#-----------------------------------------------------------------------------------------------------------------------
	#-- BEGIN LOOP ---------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------------------------------

	# Length column
	# -------------
	# Look only at lines with sequence in them
	# remove empty lines (previously >names)
	# remove any non-letter characters
	# calculate length
	awk '/^>/{print ""}/^[a-zA-Z-]/{print $1}' "$INPUTLOOP" |\
	sed /^$/d                                            |\
	sed s/[^A-Z]//g                                      |\
	awk '{print length}'                                 >Length__csv_"$i".tmp
	# Note, cysteines have been assumed to be in a disulphide state and so removed in Var1 calculations

	# "$VAR1" column
	# --------------
	# Look only at lines with sequence in them
	# remove empty lines (previously >names)
	# remove gaps, Xs and cysteines (assumed to be disulhide bonded)
	# replace each amino acid with its "$VAR1" data value   
	# replace empty lines with 1E-100 to prevent sum/n dividing by zero (i.e. all gap sequences will give value=1E-100)
	# calculate average "$VAR1"
	awk '/^>/{print ""}/^[a-zA-Z-]/{print $1}' "$INPUTLOOP"                          |\
	sed /^$/d                                                                     |\
	sed s/[CX-]//g                                                                |\
	sed s/[^A-Z]//g                                                               |\
	sed s/A/"$A"/g|sed s/C/"$C"/g|sed s/D/"$D"/g|sed s/E/"$E"/g|sed s/F/"$F"/g    |\
	sed s/G/"$G"/g|sed s/H/"$H"/g|sed s/I/"$I"/g|sed s/K/"$K"/g|sed s/L/"$L"/g    |\
	sed s/M/"$M"/g|sed s/N/"$N"/g|sed s/P/"$P"/g|sed s/Q/"$Q"/g|sed s/R/"$R"/g    |\
	sed s/S/"$S"/g|sed s/T/"$T"/g|sed s/V/"$V"/g|sed s/W/"$W"/g|sed s/Y/"$Y"/g    |\
	sed s/^$/1E-100/g                                                             |\
	awk '{OFS=","} {sum=0; n=0; for (i=1;i<=NF;i++) {sum+=$i; ++n} print sum/n}'  >"$VAR1"_csv_"$i".tmp

	# "$VAR2" column
	# --------------
	# As "$VAR1" column, using "$VAR2" data values
	# only insert values for D,E,K,R. All other letters-->0
	# sum charges rather than average
	awk '/^>/{print ""}/^[a-zA-Z-]/{print $1}' "$INPUTLOOP"                              |\
	sed /^$/d                                                                         |\
	sed s/[^A-Z]//g                                                                   |\
	sed s/D/"$D3"/g|sed s/E/"$E3"/g|sed s/K/"$K3"/g|sed s/R/"$R3"/g                   |\
	sed s/[A-Z]/" 0"/g                                                                |\
	sed s/^$/1e-100/g                                                                 |\
	awk '{OFS=","} {sum=0; n=0; for (i=1;i<=NF;i++) {sum+=$i; ++n} print sum}'        >"$VAR2"_csv_"$i".tmp

	#-----------------------------------------------------------------------------------------------------------------------
	#-- END LOOP -----------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------------------------------

done


#Combine clolumns, separating with commas
paste -d ,        \
names.tmp         \
Length__csv_0.tmp \
"$VAR1"_csv_0.tmp \
"$VAR2"_csv_0.tmp \
Length__csv_8.tmp \
"$VAR1"_csv_8.tmp \
"$VAR2"_csv_8.tmp \
Length__csv_1.tmp \
"$VAR1"_csv_1.tmp \
"$VAR2"_csv_1.tmp \
Length__csv_2.tmp \
"$VAR1"_csv_2.tmp \
"$VAR2"_csv_2.tmp \
Length__csv_3.tmp \
"$VAR1"_csv_3.tmp \
"$VAR2"_csv_3.tmp \
Length__csv_4.tmp \
"$VAR1"_csv_4.tmp \
"$VAR2"_csv_4.tmp \
Length__csv_5.tmp \
"$VAR1"_csv_5.tmp \
"$VAR2"_csv_5.tmp \
Length__csv_6.tmp \
"$VAR1"_csv_6.tmp \
"$VAR2"_csv_6.tmp \
Length__csv_7.tmp \
"$VAR1"_csv_7.tmp \
"$VAR2"_csv_7.tmp \
Length__csv_9.tmp \
"$VAR1"_csv_9.tmp \
"$VAR2"_csv_9.tmp >>header.tmp

# Cleanup
mv header.tmp Loop_statistics.csv
mv loop0.fa Full_sequence.fa
rm loop8.fa
rm loop9.fa
rm *.tmp
# Data dump
x=$(date +%y%m%d_%H%M)
mkdir               Loops_"$x"
mv loop*.fa         Loops_"$x"
mv *ter.fa          Loops_"$x"
mv Full_sequence.fa Loops_"$x"
mkdir               Columns_"$x"
mv column*.fa       Columns_"$x"

exit 0
