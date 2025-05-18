echo Initializing User Data

mkdir -p json
mkdir -p records/details

echo "Date,Start Time,End Time,Start Address,End Address,Total Miles,Purpose,Raw GPS File,Map View" >> records/master.csv



echo "This data was auto-generated based off dashcam footage. See: https://github.com/PsychedelicPalimpsest/dashcam-millage-tracking for more information" > records/README.txt
echo "LEGAL NOTICE: This data is highly confidential and contains personal information. 
Unauthorized access, use, or redistribution is strictly prohibited. Redistribution 
or sharing of this data without explicit written permission from its owner may 
result in severe legal consequences, including penalties and prosecution under 
applicable laws." > records/NOTICE
