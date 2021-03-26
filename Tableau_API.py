# -*- coding: utf-8 -*-
"""
Date: 26th March 2021
Owner: AMIT SINGH

This is a python script file to get Tableau Server Users with 
REST API and Python.
"""

# Importing necessary python libraries
import pandas as pd
import tableauserverclient as TSC
import re

# Function to check if Email ID Provide is valid
def isValidEmail(email):  
    email_regex = "^[a-z0-9_.-]+@[a-z0-9]+\.[a-z0-9.]+$"
    if(re.search(email_regex,email)):  
        return True          
    else:  
        return False
    
# Getting ableau Server Users using REST API
def getTableauServerUsers(server_url, mytoken_name, mytoken_secret, site=''):
    server = TSC.Server(server_url, use_server_version=True)
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=mytoken_name, personal_access_token=mytoken_secret, site_id=site)
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        print('[Logged in successfully to {}]'.format(server_url))

        print('[Loading users...]')
        tableauUsers = []
        for user in TSC.Pager(server.users.get):
            tableauUsers.append(
            ( user.id
             ,user.name.lower().strip()  if user.name and isinstance(user.name,str) else None
             ,user.email.lower().strip() if user.email and isinstance(user.email,str) else None
             ,user.domain_name
             ,user.fullname
             ,user.site_role
             ,user.last_login
            ))
        print('[Tableau users loaded]')
        return tableauUsers
    
# Server Login With a local admin user created directly in Tableau Server
server_url = 'https://prod-apnortheast-a.online.tableau.com'
user = '**********@gmail.com'
password = '**********'
site = 'ABCDEFGHIJ'

tableau_auth = TSC.TableauAuth(username=user, password=password, site_id=site)
server = TSC.Server(server_url, use_server_version=True)

with server.auth.sign_in(tableau_auth):
    print('[Logged in successfully to {}]'.format(server_url))
    
# Server Login using Personal Access Token (PAT)
server_url = 'https://prod-apnortheast-a.online.tableau.com'
site = 'ABCDEFGHIJ'
mytoken_name = 'ABCDEFGHIJ'
mytoken_secret = '**********yiveGu5++EmA==:3V3zWS1S9jiuRkswMV7Tgj**********'

server = TSC.Server(server_url, use_server_version=True)
tableau_auth = TSC.PersonalAccessTokenAuth(token_name=mytoken_name, personal_access_token=mytoken_secret, site_id=site)
with server.auth.sign_in_with_personal_access_token(tableau_auth):
    print('[Logged in successfully to {}]'.format(server_url))

# DataFrame with the list of users from the Tableau Server
dfTableau = pd.DataFrame(
    getTableauServerUsers(server_url = 'https://prod-apnortheast-a.online.tableau.com',
                          mytoken_name = 'ABCDEFGHIJ',
                          mytoken_secret = '**********yiveGu5++EmA==:3V3zWS1S9jiuRkswMV7Tgj**********',
                          site = 'ABCDEFGHIJ'),
    columns = ['id', 'name', 'server_email', 'domain_name', 'fullname', 'site_role', 'last_login'])

dfTableau['server_valid_email'] = dfTableau['name'].apply(isValidEmail)
dfTableau['last_login'] = dfTableau['last_login'].apply(lambda a : pd.to_datetime(a).date())

# Get all Users
print (dfTableau)
