#!/bin/bash

#----------------------------------------------------------
#
#  Creating XYZ file from Gaussian OUTPUT files '.log'
#
#----------------------------------------------------------

for file in $(ls *.log);
do
   #- rename
   gfile=$(echo $file | sed 's/.log//')

   echo "creating file ${gfile}.xyz from last geometry found in '$file'"

   # avoiding overwrite an exinting file
   if [ -s "${gfile}.xyz" ]; then
      mv ${gfile}.xyz ${gfile}.$(date +%F.%N)
#      rm ${gfile}.xyz
      echo "old file was renamed to: '${gile}.xyz.$(date +%F.%N)'"
   fi

   #- number of atoms
   natoms=$(sed -n "/Redundant/,/Recover/p" $file | sed  '/Recover/d' | wc -l)
   chk=$(grep "Redundan" $file | wc -l ) 
   natoms=$( echo "scale=0; ($natoms/$chk) - 1" | bc)

   #- reading atom list
   atomslist0=($(sed -n "/Redundant/,/Recover/p" $file | sed  '/Recover/d' | tail -$natoms))

   # What was done?
   comment="file '$file' at: ---'"$(grep "\#" $file | head -n 1 )"'---"

   # number of atoms
   tot=$(echo "${#atomslist0[@]}")

   #saving coordinates
   unset atomslist
   for (( a=0; a<$tot; a++));
   do
      atomslist+=($(echo "${atomslist0[a]}" | sed 's/,0,/,/'))
   done

   # creating coordinates XYZ file
   echo "$tot"  >> ${gfile}.xyz
   echo "    $comment" >> ${gfile}.xyz
   for ((j=0; j<$tot; j++));
   do
      coord=($( echo ${atomslist[j]} | sed 's/,/ /g' ))
      printf "%-3s   %14s   %14s   %14s\n" "${coord[0]}" "${coord[1]}" "${coord[2]}" "${coord[3]}" >> ${gfile}.xyz
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



