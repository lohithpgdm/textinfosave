import pandas as pd
import numpy as np
import streamlit as st
import time
from io import BytesIO
import os
from datetime import datetime



File_name = 'expenses.csv'

class ExpenseManager:
    def __init__(self):
        if not os.path.exists(File_name):
            df = pd.DataFrame(
                columns=['Date','Category','Description','Amount']
            )

            df.to_csv(File_name,index=False)

    
    def add_expense(self,category, description, amount):
        new_row = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Category': category,
            'Description': description,
            'Amount': amount
        }

        df = pd.read_csv(File_name)

        df = pd.concat([df,pd.DataFrame([new_row])],
                       ignore_index=True)
        
        df.to_csv(File_name,index=False)

    
    def get_data(self):
        return pd.read_csv(File_name)


    def delete_expense(self,index):
        df = pd.read_csv(File_name)

        if index<len(df):
            df = df.drop(index)
            df.to_csv(File_name,index=False)

    def total_expense(self):
        df = self.get_data()

        if len(df)==0:
            return 0
        
        return df['Amount'].sum()


