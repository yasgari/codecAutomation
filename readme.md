# Codec Automation
This script allows an agency to automate Name/PMR pairs for Webex Codec devices. Given an Excel (xlsx) spreadsheet of codec info, employee names and their PMR addresses, this script will push the info to the codec devices. Once it's complete, a user could go to the touch panel, click on a name and call the employee's personal meeting room.

## Contacts
* Yashar Asgari: yasgari@cisco.com
* Luis Velasco: luvelasc@cisco.com

## Solution Components
* Python (Pandas for Excel parsing, Requests for API call)
* Webex Codec API

## How to use

### Running Windows Executable  

#### 1. Click on the green button "Code" above, and download as ZIP file. Unzip the folder.  
#### 2. Navigate to the "Dist" folder then, "addFinal"
#### 3. Open the "names.xlsx" and "codecIPs.xlsx" files. Names.xlsx is the file that you should add the employee's names and PMRs to (using the columns provided), codecIPs.xlsx is where you should input the IP's, username, and passwords for the codecs we'd like to push these contacts to. Be sure to save both files before proceeding.
#### 4. Double click on "addFinal.exe" in the same folder, the program will run.   

### Setting up Development environment (optional for Windows users)


#### Clone the repo OR click on the green button "Code" above, and download as a ZIP file, then unzip.
```
$ git clone https://github.com/yasgari/codecAutomation
```

#### Open up Terminal in the newly created folder (unzipped or cloned from Github)  


#### Ensure Python3 is installed on your machine. Linux based OS have it by default, but Windows does not
Link for how to install Python3 on your Windows machine: https://helpdeskgeek.com/how-to/how-to-use-python-on-windows/  


#### Set up virtual environment
Create and Enter a Virtual Environment (MacOS and Linux)
```
$ python3 -m venv <NAME>
$ source <NAME>/bin/activate
```

Create and Enter a Virtual Environment (Windows)
```
$ py -m venv <NAME>
$ .\env\Scripts\activate
```


#### Install Python modules
Use pip3 to install the requirements listed in the requirements.txt file
```
$ pip3 install -r requirements.txt
```

#### Create Excel Sheets (or use templates provided)
* One Excel (xlsx) sheet should include the IP addresses, Username and Passwords for the codec that are targeted to be updated. Please name this file "names" (file extension 'xlsx') and formatted like so:  
  | IP |  user |  password  |


* The second Excel (xlsx) sheet should include the Names and PMRs (URIs) that will be added to each codec. Please name this file "codecIPs" (file extension 'xlsx') and formatted like so:  
  |  Name | PMR |


Be sure to save these two Excel sheets in the same folder as this document (readme, addFinal.py)

#### Run the script
```
$ python3 addFinal.py
```

* The script will create a folder called "PMR" and then add the contacts supplied in the "names.xlsx" spreadsheet.
* 'logs.txt' file will be created in the same folder. You can investigate the status of each API call to check for errors, etc. if needed.