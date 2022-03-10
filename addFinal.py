from venv import create
import requests
import base64
import pandas as pd
import xml.etree.ElementTree as ET


d = pd.read_excel('codecIPs.xlsx').to_dict('index')


codecInfo = []

for codec in d.values():
    
    codec['IP'] = codec['IP'].replace(u'\xa0', u'')
    codecInfo.append(codec)


print(codecInfo)

# Import Excel doc with Names, PMRs

d = pd.read_excel('names.xlsx').to_dict('index')

names = []

for name in d.values():
    names.append(name)

print(names)


# This function is where the magic happens. I am using request to open the xml file and then posting the content
# to the url of each TP endpoint based on the IP address obtained from the CSV file
# NB that http needs to be enabled on the TP endpoint otherwise you will get a 302 error.
def do_upload(aDestDevice, person, folderId):

        try:
            Logfile="logs.txt"
            
            #create XML payload for adding a name and associating it with the PMR folder created earlier.
            payload = '''<?xml version="1.0"?>
            <Command>
                <Phonebook>
                    <Contact>

                        <Add>
                            <Name>{name}</Name>
                            <FolderId>{folderId}</FolderId>
                        </Add>
                    </Contact>
                
                </Phonebook>
            </Command>
            '''.format(name = person['Name'], folderId = folderId)
            url = "http://{}/putxml".format(aDestDevice['IP'])

            #create authentication header for the API call
            userpass = aDestDevice['user'] + ':' + aDestDevice['password']
            encoded_u = base64.b64encode(userpass.encode()).decode()
            headers = {
                'Content-Type': 'text/xml',
                'Authorization': 'Basic '+encoded_u,
                'Content-Type': 'text/plain'
            }
            print('-'*40)
            print('Adding contact {name} to Codec {ip}'.format(name = person['Name'], ip = aDestDevice['IP']))
            
            #Execute API call
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            print(response.text)

            #Grab the contactId from the newly made Contact above to use below in payload2
            root = ET.fromstring(response.content)
            print(root[0][0].text)
            contactId = root[0][0].text

            #write to logfiles
            with open(Logfile, "a+") as text_file:
                text_file.write("\nThe Status of adding contact {name} to Codec {ip} |---->>>".format(name = person['Name'], ip = aDestDevice['IP'] + '\n'))
                text_file.write(response.text)


            #Now we need to associate the newly created contact above with their PMR URI
            payload2= '''<?xml version="1.0"?>
                <Command>
                    <Phonebook>
                        <ContactMethod>
                            <Add>
                                <ContactId>{contactId}</ContactId>
                                <number>{PMR}</number>
                            </Add>
                        </ContactMethod>
                    
                    </Phonebook>
                </Command>

            '''.format(contactId = contactId, PMR = person['PMR'])
            print('-' * 40)
            print('Pairing {name} to their PMR {PMR} on codec {ip}'.format(name = person['Name'], PMR = person['PMR'], ip = aDestDevice['IP']))

            #Execute API call to associate PMR with name.
            response = requests.request("POST", url, headers=headers, data=payload2, verify=False)
            print(response.text)
            with open(Logfile, "a+") as text_file:
                text_file.write('Status of pairing {name} to their PMR {PMR} on codec {ip}'.format(name = person['Name'], PMR = person['PMR'], ip = aDestDevice['IP']) + '\n')
                text_file.write(response.text)
            

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)


def createFolder(aDestDevice):
    try:
            Logfile="logs.txt"
            
            #XML payload for creating folder called 'PMR'
            payload = '''<?xml version="1.0"?>
            <Command>
                <Phonebook>
                    <Folder>
                        <Add>
                            <Name>PMR</Name>
                        </Add>
                    </Folder>
                
                </Phonebook>
            </Command>
            '''
            url = "http://{}/putxml".format(aDestDevice['IP'])

            #create authentication header for the API call
            userpass = aDestDevice['user'] + ':' + aDestDevice['password']
            encoded_u = base64.b64encode(userpass.encode()).decode()
            headers = {
                'Content-Type': 'text/xml',
                'Authorization': 'Basic '+encoded_u,
                'Content-Type': 'text/plain'
            }
            print('-'*40)
            print('Creating PMR folder on {}'.format(aDestDevice['IP']))
            
            #Execute API call
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            print(response.text)

            with open(Logfile, "a+") as text_file:
                text_file.write('Status of creating PMR folder on {}'.format( aDestDevice['IP']) + '\n')
                text_file.write(response.text)

            #Grab the folderId to pass on the next function do_upload()
            root = ET.fromstring(response.content)
            print(root[0][0].text)
            folderId = root[0][0].text
            return(folderId)

    except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)



def main():
    #Iterate through list of Codecs, and add the names/PMRs to each of them
    for codec in codecInfo:
        #create Folder called PMRs
        folderId = createFolder(codec)
        #add users/pmr grouping to the PMR folder
        for person in names:
            do_upload(codec, person, folderId)
    
    print("Finished executing script. Please view the newly made file in this folder titled 'logs.txt' to see the logs")
main()