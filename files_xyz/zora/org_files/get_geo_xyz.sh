#!/bin/bash

echo -e "\n getting coordinates from XYZ file"

if [ -z "$1" ]; then
  while :
  do
     echo -e " \n file name (.xyz) to get the coordinates from"
     read fname

     if [ ! -z "$fname" ]; then
        break
     fi

  done
else
   fname="$1"
fi
echo -e " file to get coordinates: '$fname'\n\n"

cp -f $fname data.tmp

lines=$(grep "Hg" data.tmp | wc -l)

n=1 ; l=1 ; mot=0

for (( i=0; i<$lines; i++ ));
do
   atoms=$(sed -n "${l}p" data.tmp | awk '{printf ("%i",$1)}')
   comment=$(sed -n "$(($l+1))p" data.tmp )
   coord=($(sed -n "$(($l+2)),$(($l+$atoms+1))p" data.tmp ))

   #- next line
   l=$((l + atoms + 2))

   #- counting motives for the same molecularity
   n0=$(echo "scale=0; (${atoms}-1)/3" | bc)
   if (( n==n0 )); then 
      ((mot++))
   else
      mot=1
   fi
   n="${n0}"

   #- creating gaussian input file
   gfile="w${n}s${mot}"

   if [ -s "${gfile}.com" ]; then
      mv ${gfile}.com ${gfile}.com.$(date +%F.%N)
#      rm ${gfile}.com
      echo "old file was renamed to: '${gfile}.com.$(date +%F.%N)'"
   fi

   echo "  $atoms" >> ${gfile}.xyz
   echo "  $comment" >> ${gfile}.xyz
   a=$(echo "scale=0; ($atoms)*4" | bc)
   for ((j=0; j<$a; j+=4));
   do
      x=$((j+1))
      y=$((j+2))
      z=$((j+3))
      printf "%-3s   %15.10f   %15.10f   %15.10f\n" "${coord[j]}" "${coord[x]}" "${coord[y]}" "${coord[z]}" >> ${gfile}.xyz
   done
done

rm data.tmp



#########################
exit 0
