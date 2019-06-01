now=`date +%Y-%m-%d-%H_%M_%S`
file_name="output_$now-$1_$2_$3_$4_$5.txt"
echo $now
echo $file_name
time node collect_reviews.js $1 $2 $3 $4 $5 $6 > $file_name; grep 'id:' $file_name | wc -l; grep '\[\]' $file_name | wc -l; tail $file_name; 
