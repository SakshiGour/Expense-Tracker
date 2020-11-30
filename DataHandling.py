# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 14:02:27 2020

@author: saksh
"""
import pandas as pd
from datetime import datetime
import os

# creates expenses folder if it doesn't exist
if not os.path.exists('Expenses'):
    os.makedirs('Expenses')

# creates user details file if it doesn't exist
if not os.path.exists('userdetails.csv'):
    columns = ["Username", "Password"]
    user1_exp = pd.DataFrame(columns = columns)
    user1_exp.to_csv('userdetails.csv')

# Accepting data from the user and storage
# creating a csv file for data storage
def create_csv(username):
    columns = ["Date", "Transaction Category", "Amount", "Date of Transaction", "Memo"]
    path = r'Expenses/'+ username +'.csv'
    user1_exp = pd.DataFrame(columns = columns)
    user1_exp["Date"] = pd.to_datetime(user1_exp["Date"])
    user1_exp["Date of Transaction"] = pd.to_datetime(user1_exp["Date of Transaction"])
    user1_exp["Amount"] = pd.to_numeric(user1_exp["Amount"])
    user1_exp.to_csv(path)


# Adding values to dataframe
def add_record(user, tc, amt, dtt, memo):
    path = r'Expenses/'+ user +'.csv'
    user1_exp = pd.read_csv(path)
    #dtt = datetime.strptime(dtt, '%m/%d/%Y')
    amt = float(amt)
    input_exp = pd.DataFrame({"Date":[datetime.now()],
                              "Transaction Category":[tc],
                              "Amount":[amt],
                              "Date of Transaction":[dtt],
                              "Memo":[memo]})
    user1_exp = user1_exp.append(input_exp)
    user1_exp.to_csv(path, index=False)


# check if username exists
def check_user(username):
    exists = False
    path = 'userdetails.csv'
    userdata = pd.read_csv(path)
    for row in userdata.Username:
        if row == username:
            exists = True
    return exists


# Add username and password to username and password file
def add_user(username, password):
    path = 'userdetails.csv'
    userdata = pd.read_csv(path)
    new_user = pd.DataFrame({'Username':[username],
                                 'Password':[password]})
    userdata = userdata.append(new_user)
    userdata.to_csv(path, index=False)


# check if username and password match
def check_userpass(username, password):
    exists = False
    path = 'userdetails.csv'
    userdata = pd.read_csv(path)
    for i in range(len(userdata.Username)):
        if userdata.Username[i] == username and userdata.Password[i] == password:
            exists = True
    return exists
            