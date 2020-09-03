#!/bin/bash

dirac_file="$1"

b=$(echo $dirac_file | sed 's/.out//')

output="opt_geom_"$dirac_file".xyz"

num_structures=$(grep "Cartesian coordinates in XYZ format" $dirac_file | wc -l)

# - getting geometries after opt steps
sed -n '/Cartesian coordinates in XYZ format (Angstrom)/,/Interatomic separations (in Angstroms)/p' $dirac_file > $output
# - deleting extra lines before XYZ coordinates
sed -i "/Cartesian coordinates/,+2d" $output
# - deleting extra lines after XYZ coordinates
tac $output | sed "/Interatomic separations/,+2d" | tac > new_$output
mv new_$output $output

atoms=$(head -n 1 $output | sed 's/ //g')

if (( $atoms < 1 )); then
    exit 1
fi

# - number of lines per structure
atoms=$(echo "$atoms + 2"| bc )


if [ -f "new_$output" ]; then
    rm -rf new_$output
fi

structures="20"

for (( i=0 ; i<$num_structures ; i+=$structures ));
do
    start=$(echo "1+($i*$atoms)" | bc -l)
    end=$(echo "$atoms*($i+1)" | bc -l)

    sed -n "$start, $end p" $output >> new_$output
    sed -i "s/^[[:space:]]*$/   structure $i/" new_$output

done
