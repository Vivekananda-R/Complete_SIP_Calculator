import streamlit as st
import random
import os

from files.SIP_Calculator_Functions import *

st.set_page_config(layout="wide",page_title="SIP Calculator",initial_sidebar_state="expanded")
st.title('SIP Calculator')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            </style>
            """
#To reduce the whitespace at the top of the page
st.markdown("""
        <style>
               section.block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.markdown(hide_st_style, unsafe_allow_html=True)

col1, col2 = st.columns([2,1])

with st.sidebar:
    range=st.checkbox('Return Range',value=False)
    number_input=st.checkbox('Number Input',value=False)
    initial_corpus=st.checkbox('Inital Amount',value=False)
    step_up=st.checkbox('Step Up SIP',value=False)
with col1:
    if range:
        start_rr_str='Min Return Rate Expected'
        if number_input:
            start_return_rate=st.number_input('Min Return Rate Expected',min_value=0.5,max_value=50.0,value=5.0,step=0.5,key=3)
            end_return_rate=st.number_input('Max Return Rate Expected',min_value=0.5,max_value=50.0,value=10.0,step=0.5,key=2)
        else:
            start_return_rate=st.slider('Min Return Rate Expected',min_value=0.5,max_value=50.0,value=5.0,step=0.5,key=3)
            end_return_rate=st.slider('Max Return Rate Expected',min_value=0.5,max_value=50.0,value=10.0,step=0.5,key=2)
    else:
        start_rr_str='Return Rate'
        if number_input:
            start_return_rate=st.number_input('Return Rate',min_value=0.5,max_value=50.0,value=10.0,step=0.5,key=1)
        else:
            start_return_rate=st.slider('Return Rate',min_value=0.5,max_value=50.0,value=10.0,step=0.5,key=1)
        end_return_rate=start_return_rate
    if number_input:
        principal_amount=st.number_input('Monthly SIP Amount',min_value=500,max_value=1000000,value=5000,step=500,key=4)
        period=st.number_input('Period',min_value=1,max_value=100,value=10,step=1,key=9)
        if initial_corpus:
            initial_amount=st.number_input('Initial Amount',min_value=100,max_value=10000000,value=10000,step=500,key=5)
        if step_up:
            step_up_percentage=st.number_input('Step Up Rate',min_value=0.5,max_value=100.0,value=10.0,step=0.5,key=6)
            step_up_year=st.number_input('Step Up year',min_value=1,max_value=50,value=1,step=1,key=7)
            step_up_limit=st.number_input('Step Up amount limit',min_value=10000,max_value=1000000,value=1000000,step=500,key=8)
    else:
        principal_amount=st.slider('Monthly SIP Amount',min_value=500,max_value=1000000,value=5000,step=500,key=4)
        period=st.slider('Period',min_value=1,max_value=100,value=10,step=1,key=9)
        if initial_corpus:
            initial_amount=st.slider('Initial Amount',min_value=100,max_value=10000000,value=10000,step=500,key=5)
        
        if step_up:
            step_up_percentage=st.slider('Step Up Rate',min_value=0.5,max_value=100.0,value=10.0,step=0.5,key=6)
            step_up_year=st.slider('Step Up year',min_value=1,max_value=50,value=1,step=1,key=7)
            step_up_limit=st.slider('Step Up amount limit',min_value=10000,max_value=1000000,value=1000000,step=500,key=8)
    
if not(initial_corpus):
    initial_amount=0
if not(step_up):
    step_up_percentage=0
    step_up_year=1
    step_up_limit=0

submit=st.button('Submit')
if __name__ == '__main__': 
    if submit:
        result,yearly_calculations=future_value(principal_amount=principal_amount,calculated_return_rate=range,
                            start_return_rate=start_return_rate,end_return_rate=end_return_rate,
                            initial_amount=initial_amount,period=period,
                            annual_stepup=step_up_percentage,stepup_everyyear=step_up_year,
                            max_stepup_limit=step_up_limit,print_result=False)
        result['Base Monthly amount']=principal_amount
        if initial_corpus:
            result['Initial Invested']=initial_amount
        if step_up:
            result['Step Up Percentage %']=step_up_percentage
            result['Step Up every']=f'{str(step_up_percentage)} year'
            result['Step Up limit']=step_up_limit
        print(result)
        show_result(result,yearly_calculations)


