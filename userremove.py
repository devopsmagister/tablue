# Retrieve the user you want to delete:
user_filter = TSC.RequestOptions()
user_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, 'username'))
users, _ = server.users.get(req_options=user_filter)
user_id = users[0].id  # Assuming there's only one user with the provided username

# Retrieve the new owner user:
new_owner_filter = TSC.RequestOptions()
new_owner_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, 'new_owner_username'))
new_owners, _ = server.users.get(req_options=new_owner_filter)
new_owner_id = new_owners[0].id  # Assuming there's only one user with the provided new owner username



# Check if the user is the owner of any workflows:
owner_filter = TSC.RequestOptions()
owner_filter.filter.add(TSC.Filter(TSC.RequestOptions.Field.OwnerId, TSC.RequestOptions.Operator.Equals, user_id))
workflows, _ = server.workflows.get(req_options=owner_filter)
if workflows:
    # The user is the owner of one or more workflows
    # Decide how to handle this scenario (e.g., reassign ownership or delete workflows)
    workflow.owner_id = new_owner_id
    server.workflows.update(workflow)


# Delete user
server.users.delete(user_id)
server.auth.sign_out()
