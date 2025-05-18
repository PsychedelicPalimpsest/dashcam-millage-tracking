echo Initializing User Data

mkdir -p json
mkdir -p records/details

echo "Date,Start Time,End Time,Start Address,End Address,Total Miles,Purpose,Raw GPS File,Map View" >> records/master.csv



echo "This data was generated based off dashcam footage. " > records/README.txt