# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 04:06:44 2020

@author: saksh
"""


import pandas as pd

# visualization of monthly transactions
def monthly_transactions(username):
    path = r'Expenses/'+username+'.csv'
    df = pd.read_csv(path)
    
    df.index = pd.to_datetime(df['Date of Transaction'])
    df['Date'] = pd.to_datetime(df['Date'])
    gb = df.groupby(by=[df.index.month, df.index.year]).sum()
    gb.plot(kind='bar', y='Amount', rot=0,
                title="Montly distribution of Total Expenses").set(xlabel="Month, Year", 
                                                                   ylabel="Amount ($)")
# visualization of category-wise transactions
def category_transactions(username):
    path = r'Expenses/'+username+'.csv'
    df = pd.read_csv(path)
    
    df.index = pd.to_datetime(df['Date of Transaction'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    cat = df.groupby(df['Transaction Category']).sum()
    cat.plot.pie(y='Amount', title="Category-wise Distribution of Total Expenses",
                 autopct='%1.1f%%', figsize=(8,8))
    
