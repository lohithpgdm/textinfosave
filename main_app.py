import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ExpenseManager

st.set_page_config(
    page_title='Expense Tracker',
    page_icon = '💎',
    layout = 'wide'
)

manager = ExpenseManager()

st.title('Personal Expense Tracker')

st.sidebar.header('Add Expense')

with st.sidebar.form('expense form'):
    category = st.selectbox(
        'category',[
            'Food',
            'Travel',
            'Shopping',
            'Bills',
            'Entertainement',
            'Others'
        ]
    )


    description = st.text_input('Description')

    amount = st.number_input(
        'Amount',
        min_value = 0,
        step=1
    )

    submit = st.form_submit_button('Add Expense')

    if submit:
        manager.add_expense(category,description,amount)

        st.sidebar.success('Expense Added')

df=manager.get_data()


tab1,tab2,tab3 = st.tabs(['Dashboard','Expenses','Analytics'])

with tab1:
    total = df['Amount'].sum() if not df.empty else 0
    food = (df[df['Category']=='Food']['Amount'].sum() if not df.empty else 0)
    travel = (df[df['Category']=='Travel']['Amount'].sum() if not df.empty else 0)
    

    c1,c2,c3 = st.columns(3)

    c1.metric('Total Expense',f'₹{total:,.0f}')
    c2.metric('Food Expense',f'₹{food:,.0f}')
    c3.metric('Travel Expense',f'₹{travel:,.0f}')


with tab2:
    st.subheader('Expense Records')
    st.dataframe(df,use_container_width=True)
    st.download_button(label='Download csv',data=df.to_csv(index=False),file_name = 'expenses.csv',mime='text/csv')

with tab3:
    if not df.empty:
        cat_df = (df.groupby('Category')['Amount'].sum().reset_index())
        pie = px.pie(cat_df,values='Amount',names='Category',title='Category wise spending')
        st.plotly_chart(pie,use_container_width=True)

        bar = px.bar(cat_df,x='Category',y='Amount',title='Expenses by Category')
        st.plotly_chart(bar,use_container_width=True)

    else:
        st.info('Add expenses to view analytics')


with st.expander('View Raw data'):
    st.write(df)