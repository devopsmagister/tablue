import requests
from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET

server_name = "prod-useast-b.online.tableau.com"
version = "3.20"
username = "yyyyy@gmail.com"
password = "xxxxxxx"

signin_url = "https://{server}/api/{version}/auth/signin".format(server=server_name, version=version)
signout_url = "https://{server}/api/{version}/auth/signout".format(server=server_name, version=version)

#Create data for api
request_xml = ET.Element('tsRequest')
credentials = ET.SubElement(request_xml, 'credentials',
name=username, password=password)
site_element = ET.SubElement(credentials, 'site', contentUrl="Test123")

request_data = ET.tostring(request_xml)

response = Request(signin_url, data=request_data, method="POST")

req = urlopen(response)

# Get the response
server_response = req.read()

response_xml = ET.fromstring(server_response)

# Get the credentials token from the <credentials> element
token = response_xml.find('.//t:credentials',
			namespaces={'t': "http://tableau.com/api"}).attrib['token']

# Get the site ID from the <site> element
site_id = response_xml.find('.//t:site',
			namespaces={'t': "http://tableau.com/api"}).attrib['id']

print('Sign in successful!')

# Set the authentication header using the credentials token returned by the Sign In method.
headers = {'X-tableau-auth': token}


# User details
new_user_name = "xxxx@gmail.com"
new_user_role = "SiteAdministratorCreator"  # Role you want to assign

# Create the user
user_create_url = "https://{server}/api/{version}/sites/{site_id}/users".format(server=server_name, version=version, site_id=site_id)

# headers = {
#     "Content-Type": "application/json",
# }

data = {
    "user": {
        "name": new_user_name,
        "siteRole": new_user_role,
    }
}

response = requests.post(user_create_url, json=data, headers=headers)

if response.status_code == 201:
    print("User created successfully.")
else:
    print("User creation failed. Status code:", response.status_code)
    print(response.text)


# Sign out
signout_url = "https://{server}/api/{version}/auth/signout".format(server=server_name, version=version)
req = Request(signout_url, headers=headers, data=b'')
req = urlopen(req)
print('Sign out successful!')