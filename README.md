# Adhrit
Adhrit is an open source Android APK ripping tool that does a basic recon on the provided APK file. Built mainly with CTFs on focus. 

## Uses :

1. Extracts the apk contents.
2. Searches for native libraries.
3. Extracts jar out of dex.
4. Extracts source code in Java.
5. Analyzes permissions used by the application.
6. Dumps the Manifest.
7. Dumps the certificate details.
8. Checks for malware footprints in VirusTotal database. 


## Pre-requisites :

1. Linux Machine or MAC
2. Java JDK


## Usage :

1. Dowload or clone the package and extract the tool.
2. Place the application in the tool directory. 
3. Open a terminal and cd into the directory.
4. Run "python adhrit.py -a your_app.apk" 
