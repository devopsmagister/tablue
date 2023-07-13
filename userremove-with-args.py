####
# This script demonstrates how to use change ownership of an existing user
####

#python3 .\userremove.py --server https://prod-useast-b.online.tableau.com/ --site <site_name> --username '<username>' --password '<password>' --deleteuser '<delete user>' --new_owner_username "new assigne user"

import argparse
import logging
import os.path
import sys

import tableauserverclient as TSC


def main():
    parser = argparse.ArgumentParser(description="Explore site updates by the Server API.")
    parser.add_argument("--server", "-s", help="server address")
    parser.add_argument("--site", "-S", help="site name")
    parser.add_argument("--username", "-p", help="name of the personal access token used to sign into the server")
    parser.add_argument("--password", "-v", help="value of the personal access token used to sign into the server")
    parser.add_argument(
        "--logging-level",
        "-l",
        choices=["debug", "info", "error"],
        default="error",
        help="desired logging level (set to error by default)",
    )

    parser.add_argument("--deleteuser")
    parser.add_argument("--new_owner_username")
    parser.add_argument("--delete")
    parser.add_argument("--create")
    parser.add_argument("--url")
    parser.add_argument("--new_site_name")
    parser.add_argument("--user_quota")
    parser.add_argument("--storage_quota")
    parser.add_argument("--status")

    args = parser.parse_args()

    # Set logging level based on user input, or error by default
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    # SIGN IN
    password = args.password or getpass.getpass("Password: ")
    tableau_auth = TSC.TableauAuth(args.username, password, site_id=args.site)
    print("\nSigning in...\nServer: {}\nSite: {}\nUsername: {}".format(args.server, args.site, args.username))

    server = TSC.Server(args.server, use_server_version=True)
    new_site = None
    with server.auth.sign_in(tableau_auth):


        # Retrieve the user you want to delete:
        user_filter = TSC.RequestOptions()
        # user_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, 'username'))
        user_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, args.deleteuser))
        users, _ = server.users.get(req_options=user_filter)
        user_id = users[0].id  # Assuming there's only one user with the provided username

        # Retrieve the new owner user:
        new_owner_filter = TSC.RequestOptions()
        # new_owner_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, 'new_owner_username'))
        new_owner_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, args.new_owner_username))
        new_owners, _ = server.users.get(req_options=new_owner_filter)
        new_owner_id = new_owners[0].id  # Assuming there's only one user with the provided new owner username

        print(user_id, new_owner_id)
        # Get all workbooks
        all_workbooks, pagination_item = server.workbooks.get()

        for workbook in all_workbooks:
            wb = server.workbooks.get_by_id(workbook.id)
            owner_id = wb.owner_id
            # Check if delete user is owner of  any workbook
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} workbooks".format(args.deleteuser, wb.name))
                            
              #Assign owner to new user
              wb.owner_id = new_owner_id
              server.workbooks.update(wb)
        
        
        # Get all projecct
        all_projects, pagination_item = server.projects.get()

        for project in all_projects:
 
            owner_id = project.owner_id
            # Check if delete user is owner of  any projecct
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} projects".format(args.deleteuser, project.name))
  
              # Assign owner to new user
              try:
                project.owner_id = new_owner_id
                server.projects.update(project)
              except NotImplementedError:
                print("\n!!!Warning!!!\nREST API does not currently support updating project owner. :() \nPlease update owner manually\n")

        # Get all Datasource
        all_datasources, pagination_item = server.datasources.get()

        for datasource in all_datasources:
            ds = server.datasources.get_by_id(datasource.id)
            owner_id = ds.owner_id
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
            print(owner_id)
            # Check if delete user is owner of any flow
            if owner_id == user_id:
              print("\nUser {0} owns or has owner permissions for {1} datasource".format(args.deleteuser, flow.name))
                            
              #Assign owner to new user
              flow.owner_id = new_owner_id
              server.datasources.update(flow)
    
        server.auth.sign_out()



if __name__ == "__main__":
    main()



