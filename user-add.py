import requests

# Tableau Server URL and authentication details
tableau_server_url = "https://your-tableau-server-url"
username = "your-admin-username"
password = "your-admin-password"

# User details
new_user_name = "newuser@example.com"
new_user_fullname = "New User"
new_user_role = "serverAdministrator"  # Role you want to assign

# Create the user
user_create_url = f"{tableau_server_url}/api/3.9/sites/{site_id}/users"

headers = {
    "Content-Type": "application/json",
}

data = {
    "user": {
        "name": new_user_name,
        "siteRole": new_user_role,
        "authSetting": "ServerDefault",  # Set authentication type
        "fullName": new_user_fullname,
    }
}

response = requests.post(user_create_url, json=data, auth=(username, password), headers=headers)

if response.status_code == 201:
    print("User created successfully.")
else:
    print("User creation failed. Status code:", response.status_code)
    print(response.text)