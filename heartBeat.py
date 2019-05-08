# Description : 
# 1. Connect with Google Drive and fethc export.zip folder
# 2. Extract export.zip folder
# 3. Read export.xml file and capture - HeartRateVariabilityMetadataList & write data into a CSV file
# File to be uploaded to this link - https://drive.google.com/drive/folders/1aoURMlMlb0DYPeI2vcM7nGKI44uMnu_I?usp=sharing
#######

# Importing required module
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from xml.dom import minidom
import os
import sys
import zipfile
import csv


# Variable Declaration
error_found     = False 
counter         = 0
occurance       = 0
current_workdir = os.getcwd()                  # Getting Current working directory Information
xmlFile         = current_workdir + '/' + 'apple_health_export' + '/' + 'export.xml'
hBFile          = current_workdir + '/' +  'heartbeat.csv'



print("+++ Message : Working Directory = " + current_workdir)

# Connecting to Google Drive
gLogin          = GoogleAuth()
gLogin.LocalWebserverAuth()                    # This opens a google login page and select account to access program
drive           = GoogleDrive(gLogin)

heartBeat       = '1aoURMlMlb0DYPeI2vcM7nGKI44uMnu_I' # Shared Folder ID - Folder Name "HearBeat"
data_files      = drive.ListFile({'q':"'"+heartBeat+"' in parents and trashed=false"}).GetList()

for file1 in data_files:
    print('+++ Message : Downloading File = %s' % (file1['title']))
    file1.GetContentFile(file1['title'])

if not os.path.isfile(current_workdir + '/' + 'export.zip'):
    print('!!! Error : Unable to locate data folder - export.zip ')
    error_found = True
else:
    # Extract zip folder
    with zipfile.ZipFile(current_workdir + '/' + 'export.zip',"r") as zip_ref:
        zip_ref.extractall()
    if not os.path.isdir(current_workdir + '/' + 'apple_health_export'):
        error_found = True
    else:
        # Read the XML File and create CSV file
        parseFile  = minidom.parse(xmlFile)
        rateVarSSDNList =  parseFile.getElementsByTagName('HeartRateVariabilityMetadataList')
        rateVarList = parseFile.getElementsByTagName('InstantaneousBeatsPerMinute')
        print('+++ Message : Parsing the XML file ')
        # Capturing HeartRateVariabilityMetadataList for multiple occurance
        '''for rVarSSDN in rateVarSSDNList:
            occurance = occurance + 1
            print('*** Occurance = ',occurance)'''
        with open(hBFile,'w') as beatFile:
            bFile = csv.writer(beatFile)
            for hRate in rateVarList:
                # Writing Header Row
                if counter == 0:
                    timeStamp = "CAPTURED TIME"
                    beatsPM   = "BPM"
                    hRow = [timeStamp,beatsPM]
                    #print(hRow)
                    bFile.writerow(hRow)
            
                # Getting the data for the file   
                timeStamp = hRate.attributes['time'].value
                beatsPM   = hRate.attributes['bpm'].value
                dRow      = [timeStamp,beatsPM]
                #print(dRow)
                bFile.writerow(dRow)
                counter = counter + 1
        if os.path.isfile(hBFile):
            print('+++ Message : CSV file - heartbeat, created at Location = ' + hBFile)
        else:
            print('!!! Warning  : Unable to locate HeartBeat.csv file')
            error_found = True
            
        

if error_found:
    print('!!! Script completed with error !!! ')
    sys.exit(1)
else:
    print('### Success : Script execution completed ###')
