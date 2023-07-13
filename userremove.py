####
# This script demonstrates how to use change ownership of an existing user
####
# export server="https://prod-useast-b.online.tableau.com/"
# export site="test"
# export username="test"
# export password="test"
# export deleteuser="delete-user"

import argparse
import logging
import os
import os.path
import sys

import tableauserverclient as TSC


def main():

    server = os.environ.get('server')
    site = os.environ.get('site')
    username = os.environ.get('username')
    password = os.environ.get('password')

    parser = argparse.ArgumentParser(description="Explore site updates by the Server API.")
    parser.add_argument(
        "--logging-level",
        "-l",
        choices=["debug", "info", "error"],
        default="error",
        help="desired logging level (set to error by default)",
    )

    parser.add_argument("--deleteuser")

    args = parser.parse_args()

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # SIGN IN
    password = password or getpass.getpass("Password: ")
    tableau_auth = TSC.TableauAuth(username, password, site_id=site)
    print("\nSigning in...\nServer: {}\nSite: {}\nUsername: {}".format(server, site, username))

    server = TSC.Server(server, use_server_version=True)
    new_site = None
    with server.auth.sign_in(tableau_auth):


        # Retrieve the user you want to delete:
        user_filter = TSC.RequestOptions()
        user_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, args.deleteuser))
        users, _ = server.users.get(req_options=user_filter)
        user_id = users[0].id 

        # Get all projecct
        all_projects, pagination_item = server.projects.get()


        for project in all_projects: 
            owner_id = project.owner_id
            # Check if delete user is owner of  any projecct
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} projects".format(args.deleteuser, project.name))
              sys.exit("Failed to channge owner of project")

        # Get all workbooks
        all_workbooks, pagination_item = server.workbooks.get()

        for workbook in all_workbooks:
            wb = server.workbooks.get_by_id(workbook.id)
            owner_id = wb.owner_id
            
            #Check if delete user is the owner of the project of workbook
            for project in all_projects: 
              if project.id == workbook.project_id:
                new_owner_id = project.owner_id
                if user_id == new_owner_id:
                  print("\nUser {0} is owner permissions for {1} workbooks's project\n".format(args.deleteuser, wb.name))
                  sys.exit("Failed to channge owner of workbook")

            # Check if delete user is owner of  any workbook
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} workbooks".format(args.deleteuser, wb.name))
                            
              #Assign owner to new user
              wb.owner_id = new_owner_id
              server.workbooks.update(wb)
        
        # Get all Datasource
        all_datasources, pagination_item = server.datasources.get()

        for datasource in all_datasources:        
            ds = server.datasources.get_by_id(datasource.id)
            owner_id = ds.owner_id

            # Check if delete user is the owner of the project of datasource
            for project in all_projects: 
              if project.id == datasource.project_id:
                new_owner_id = project.owner_id
                if user_id == new_owner_id:
                  print("\nUser {0} is owner permissions for {1} datasource's project\n".format(args.deleteuser, ds.name))
                  sys.exit("Failed to channge owner of datasource")

            # Check if delete user is owner of any datasources
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} datasource".format(args.deleteuser, ds.name))
                            
              #Assign owner to new user
              ds.owner_id = new_owner_id
              server.datasources.update(ds)

        # Get all flow
        all_flows, pagination_item = server.flows.get()

        for flow in all_flows:
            owner_id = flow.owner_id

            # Check if delete user is the owner of the project of flow
            for project in all_projects: 
              if project.id == flow.project_id:
                new_owner_id = project.owner_id
                if user_id == new_owner_id:
                  print("\nUser {0} is owner permissions for {1} flow's project\n".format(args.deleteuser, flow.name))
                  sys.exit("Failed to channge owner of flow")

            # Check if delete user is owner of any flow
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} flow.".format(args.deleteuser, flow.name))
                            
              #Assign owner to new user
              flow.owner_id = new_owner_id
              server.datasources.update(flow)
    
        server.auth.sign_out()



if __name__ == "__main__":
    main()



