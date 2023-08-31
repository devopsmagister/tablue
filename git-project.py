import requests

# Tableau Server URL and authentication details
tableau_server_url = "https://your-tableau-server-url"
username = "your-admin-username"
password = "your-admin-password"

# Project details
project_id = "your-project-id"  # Replace with the actual project ID
new_owner_id = "new-owner-user-id"  # Replace with the new owner's user ID

# Get the current project details
project_url = f"{tableau_server_url}/api/3.9/sites/{site_id}/projects/{project_id}"
response = requests.get(project_url, auth=(username, password))

if response.status_code == 200:
    project_data = response.json()
    project_data['project']['ownerId'] = new_owner_id

    # Update the project owner
    update_response = requests.put(project_url, json=project_data, auth=(username, password))

    if update_response.status_code == 200:
        print("Project owner updated successfully.")
    else:
        print("Project owner update failed. Status code:", update_response.status_code)
        print(update_response.text)
else:
    print("Failed to fetch project details. Status code:", response.status_code)
    print(response.text)