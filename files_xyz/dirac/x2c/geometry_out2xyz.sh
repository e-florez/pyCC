#!/bin/bash

#----------------------------------------------------------
#
#  Creating XYZ file from Gaussian OUTPUT files '.log'
#
#----------------------------------------------------------

for file in $(ls *.out);
do
   #- rename
   gfile=$(echo $file | sed 's/.out//')

   echo "creating file ${gfile}.xyz from last geometry found in '$file'"

   # avoiding overwrite an exinting file
   if [ -s "${gfile}.xyz" ]; then
      mv ${gfile}.xyz ${gfile}.xyz.$(date +%F.%N)
#      rm ${gfile}.xyz
      echo "old file was renamed to: '${gile}.xyz.$(date +%F.%N)'"
   fi

   #- number of atoms
   natoms=$(sed -n "/Final geometry (angstrom)/,/Iter          Energy     Change/p" $file | sed  '/Iter          Energy     Change/d' | sed '/^$/d' | wc -l)
   natoms=$( echo "scale=0; ($natoms) - 2" | bc)

   #- reading atom list
   atomslist=($(sed -n "/Final geometry (angstrom)/,/Iter          Energy     Change/p" $file | sed  '/Iter          Energy     Change/d' | sed '/^$/d' | tail -$natoms))

   # What was done?
   comment="file: '$file'"

   # number of atoms
   tot=$(echo "scale=0; ${#atomslist[@]}" | bc)
   tot2=$(echo "scale=0; ${#atomslist[@]}/4" | bc)

   # creating coordinates XYZ file
   echo "$tot2"  >> ${gfile}.xyz
   echo "    $comment" >> ${gfile}.xyz
   for ((j=0; j<$tot; j+=4));
   do
      printf "%-3s   %14s   %14s   %14s\n" "${atomslist[j]}" "${atomslist[j+1]}" "${atomslist[j+2]}" "${atomslist[j+3]}" >> ${gfile}.xyz
   done
done

echo -e "*** DONE\n"


#######################################
exit 0


   #- creating gaussian input file
   echo "%chk=${gfile}.chk" >> ${gfile}.com
   echo "%nproc=16" >> ${gfile}.com
   echo "%mem=100gb" >> ${gfile}.com
   echo "" >> ${gfile}.com
   echo "#p mp2=full gen pseudo=Read opt freq" >> ${gfile}.com
   echo "" >> ${gfile}.com
   echo "   file: ${gfile} from a old opt at MP2/SDALL. Now we use MP2(full)/Def2-TZVPPD" >> ${gfile}.com
   echo "" >> ${gfile}.com
   echo "2 1" >> ${gfile}.com

   for ((j=0; j<$tot; j++));
   do
      coord=($( echo ${atomslist[j]} | sed 's/,/ /g' ))
      printf "%-3s   %14s   %14s   %14s\n" "${coord[0]}" "${coord[1]}" "${coord[2]}" "${coord[3]}" >> ${gfile}.com
   done

   echo "" >> ${gfile}.com
   cat def2-TZVPPD >> ${gfile}.com

   #- list to submmit jobs
   echo "   g16 < ${gfile}.com > ${gfile}.log" >> list.dat



