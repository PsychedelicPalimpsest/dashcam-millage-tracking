echo Initializing User Data

mkdir -p json
mkdir -p records/details

echo "Date,Start Time,End Time,Start Address,End Address,Total Miles,Purpose,Raw GPS File,Map View" >> records/master.csv



echo "This data was auto-generated based off dashcam footage. See: https://github.com/PsychedelicPalimpsest/dashcam-millage-tracking for more information" > records/README.txt
echo "LEGAL NOTICE: This data contains highly sensitive and confidential financial information. 
ANY unauthorized access, use, reproduction, or redistribution is STRICTLY PROHIBITED. 
Failure to comply with this notice WILL result in severe legal action, including but not 
limited to civil and criminal penalties, as permitted under applicable laws. Access to 
this data is restricted to authorized personnel ONLY. Violators will be prosecuted to 
the fullest extent of the law." > records/NOTICE
