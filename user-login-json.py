# This example shows how to use the Tableau Server REST API
# to sign in to a server, get back a credentials token and
# site ID, and then sign out.
# The example runs in Python 2.7 and Python 3.3 code

import requests, json


# NOTE! Substitute your own values for the following variables
# use_pat_flag = True  # True = use personal access token for sign in, false = use username and password for sign in.

server = "prod-useast-b.online.tableau.com"
version = "3.20"
username = "devopsmagister@gmail.com"
password = "xxxx"

site_url = "Test123"    # Site (subpath) to sign in to. An empty string is used to specify the default site.

signin_url = "https://{server}/api/{version}/auth/signin".format(server=server, version=version)



payload = { "credentials": { "name": username, "password": password, "site": {"contentUrl": site_url }}}

headers = {
	'accept': 'application/json',
	'content-type': 'application/json'
}

# Send the request to the server
req = requests.post(signin_url, json=payload, headers=headers, verify=False)
req.raise_for_status()

# Get the response
response = json.loads(req.content)

# Get the credentials token from the credentials element
token = response["credentials"]["token"]

# Get the site ID from the <site> element
site_id = response["credentials"]["site"]["id"]

print('Sign in successful!')
# Set the authentication header using the token returned by the Sign In method.
headers['X-tableau-auth']=token
print(headers)



# ... Make other calls here ...


# Sign out
signout_url = "https://{server}/api/{version}/auth/signout".format(server=server, version=version)

req = requests.post(signout_url, data=b'', headers=headers, verify=False)
req.raise_for_status()
print('Sign out successful!')