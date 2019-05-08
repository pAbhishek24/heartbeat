# heartbeat

Python program to read heart beats provide from Healt App - from iPhone

1. Export your healt app in shared google drive 
    Folder Name - HeartBeat
    Shared Link - https://drive.google.com/drive/folders/1aoURMlMlb0DYPeI2vcM7nGKI44uMnu_I?usp=sharing
2. Program will download the 'export.zip' folder, unzip it and reads heart rate.
     2.1 HKQuantityTypeIdentifierHeartRate
     2.2 HeartRateVariabilityMetadataList
3. After reading heart rate it generates 2 CSV file
     3.1 heartbeat.csv - containing the heart beats per minute from available source
     3.2 heartbeat_metaList.csv -contains beat information per milli second

To execute program
 1. Create client_id and secrete key for the folder in which data will be placed
 2. Put your client_secret.json file in same folder as in your python file
 
 Run - heartBeat.py 
