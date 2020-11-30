# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:43:10 2020

@author: saksh
"""
import PySimpleGUI as sg
from datetime import datetime
import DataHandling
import Visualize


sg.theme('DarkTeal6')

# layout for login window
layout_login = [[sg.Text('Username: '), sg.Input(key='_username_')],
                [sg.Text('Password: '), sg.Input(key='_pass_', password_char='*')],
                [sg.Button('Login'), sg.Button('Create Account')]]

# layout for Create Account Window
layout_acc = [[sg.Text('Username: '), sg.Input(key='_userenter_')],
              [sg.Text('Password: '), sg.Input(key='_passenter_')],
              [sg.Button('Create')]]

# layout for Selecting operations
layout_tab1 = [[sg.Text(f'Date: {datetime.now()}')],
              [sg.Text('What do you want to do today?')],
              [sg.Radio('Record Transactions', 'Radio_func', default=True, key='_rectransact_'),
               sg.Radio('Visualize Expenses', 'Radio_func', key='_vizexp_')],
              [sg.Button('Next')]]

# layout for Adding new records
categories = ['Housing', 'Transportation', 'Insurance', 'Savings', 'Food', 'Utilities', 'Clothing', 'Medical/Healthcare', 'Education', 'Entertainment', 'Gifts/Donations', 'Repairs', 'Miscellaneous']
layout_tab2 = [[sg.Text(f'Date: {datetime.now()}')],
              [sg.Text('Transaction Category:'), sg.Combo(categories, key='_category_')],
              [sg.Text('Amount: $'), sg.InputText(key='_amt_')],
              [sg.Text('Date of Transaction (yyyy-mm-dd):'), sg.InputText(key='_dttransac_'), sg.CalendarButton('Select a Date', key='_dttransac_')],
              [sg.Text('Memo:'), sg.InputText(key='_memo_')],
              [sg.Button('Add'), sg.Button('Reset'), sg.Button('Back')]]   
key_list = ['_category_', '_amt_', '_dttransac_', '_memo_'] # key list for resetting

# Select plots layout
layout_frame = [[sg.Radio('Expenses by Month', 'Graph_type', key='_graphmonth_')],
                [sg.Radio('Expenses by Category', 'Graph_type', key='_graphcat_')]]
layout_tab3 = [[sg.Text(f'Date: {datetime.now()}')],      
              [sg.Frame('Select the Visualization:', layout_frame)],
              [sg.Button('Plot'), sg.Button('Back to Main Menu')],
              [sg.Text('Note: The graphs will open up in a different window.')]]

# layout to set tabs for selecting operations, adding new records and plotting window
layout_user = [[sg.TabGroup([[sg.Tab('Select Operation', layout_tab1, tooltip='tip', key='_tab1_'),
                              sg.Tab('Enter data', layout_tab2, key='_tab2_', visible=False),
                              sg.Tab('Visualization', layout_tab3, key='_tab3_', visible=False)]], tooltip='TIP2')],
               [sg.Button("Logout")]] 

# layout to switch between login, create account and the tabbed layouts
layout = [[sg.Column(layout_login, key='-COL1-'), sg.Column(layout_user, visible=False, key='-COL2-'), sg.Column(layout_acc, visible=False, key='-COL3-')],
          [sg.Exit()]]


window = sg.Window('Expense Tracker', layout, default_element_size=(20,1), location=(500,200), margins=(10,10),font='Helvetica')    



while True:    
    event, values = window.read()     
    if event == sg.WIN_CLOSED or event is None or event == 'Exit':           # always,  always give a way out!    
        break  
    if event == 'Next':                         
          if values['_rectransact_'] == True:       # make tab 2 visible
              window.FindElement('_tab2_').Update(visible=True)
              window.FindElement('_tab3_').Update(visible=False)
              window.FindElement('_tab1_').Update(visible=False)
          elif values['_vizexp_'] == True:          # make tab 3 visible
              window.FindElement('_tab3_').Update(visible=True)
              window.FindElement('_tab2_').Update(visible=False)
              window.FindElement('_tab1_').Update(visible=False)
    elif event == 'Back':                           # make tab 1 visible
         window.FindElement('_tab1_').Update(visible=True)
         window.FindElement('_tab2_').Update(visible=False)
         window.FindElement('_tab3_').Update(visible=False)
    elif event == 'Back to Main Menu':              # make tab 1 visible
         window.FindElement('_tab1_').Update(visible=True)
         window.FindElement('_tab2_').Update(visible=False)
         window.FindElement('_tab3_').Update(visible=False)
    elif event == 'Reset':                          #resetting values on the tab
         for key in key_list:
             window[key]('')
    elif event == 'Add':                            #adding data values to database
        try:
            values['_dttransac_']= datetime.strptime(values['_dttransac_'], '%Y-%m-%d %H:%M:%S')
        except:
            sg.popup('Select date through the \'Select a Date\' button.')
        else:
            try:
                DataHandling.add_record(values['_username_'], values['_category_'], values['_amt_'], values['_dttransac_'], values['_memo_'])
                sg.popup('Values Added!')
                for key in key_list:
                    window[key]('')
            except:
                sg.popup('Please enter all the right values before proceeding. Amount should be a number and shouldn\'t be left blank')
                for key in key_list:
                    window[key]('')
    elif event == 'Login':                          # login with username and password
        check = DataHandling.check_userpass(values['_username_'], values['_pass_'])
        if check == True:                           
            window['-COL1-'].Update(visible=False)
            window['-COL2-'].Update(visible=True)
            values['_user_'] = values['_username_']
        elif check == False:
            sg.popup('Error','Wrong username or password.')
            window['_username_']('')
            window['_pass_']('')
    elif event == 'Logout':                         # logout from present account
        window['-COL1-'].Update(visible=True)
        window['-COL2-'].Update(visible=False)
        window['_username_']('')
        window['_pass_']('')
        
    elif event == 'Create Account':                 # create new account
        window['-COL1-'].Update(visible=False)
        window['-COL3-'].Update(visible=True)
    elif event == 'Create':                         # create new account
        exists = DataHandling.check_user(values['_userenter_'])
        if exists == True:
            sg.popup('Username Already Exists! Please enter a new username.')
            window['_userenter_']('')
            window['_passenter_']('')
        elif exists == False:
            DataHandling.add_user(values['_userenter_'], values['_passenter_'])
            DataHandling.create_csv(values['_userenter_'])
            sg.popup('User Added! Enter login details to login to your account.')
            window['-COL1-'].Update(visible=True)
            window['-COL3-'].Update(visible=False)
    elif event == 'Plot':
        if values['_graphmonth_']==True:
            Visualize.monthly_transactions(values['_username_'])
        elif values["_graphcat_"]==True:
            Visualize.category_transactions(values['_username_'])
window.close()