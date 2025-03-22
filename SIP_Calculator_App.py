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

default_values={
    'range':False,
    'number_input':False,
    'initial_corpus':False,
    'step_up':False,
    'start_return_rate':5.0,
    'end_return_rate':10.0,
    'principal_amount':10000,
    'period':10,
    'initial_amount':100000,
    'step_up_limit':100000,
    'step_up_year':1,
    'step_up_percentage':10,
    'step_up_increment_number':False
    
    
    
}

with st.sidebar:
    range=st.checkbox('Return Range',value=default_values['range'])
    number_input=st.checkbox('Number Input',value=['number_input'])
    initial_corpus=st.checkbox('Inital Amount',value=default_values['initial_corpus'])
    step_up=st.checkbox('Step Up SIP',value=default_values['step_up'])
    if step_up:
        step_up_increment_number=st.checkbox('Step Up amount wise',value=default_values['step_up_increment_number'])
    else:
        step_up_increment_number=False
with col1:
    if range:
        start_rr_str='Min Return Rate Expected'
        if number_input:
            start_return_rate=st.number_input('Min Return Rate Expected',min_value=0.5,max_value=50.0,value=default_values['start_return_rate'],step=0.5,key=3)
            end_return_rate=st.number_input('Max Return Rate Expected',min_value=0.5,max_value=50.0,value=default_values['end_return_rate'],step=0.5,key=2)
        else:
            start_return_rate=st.slider('Min Return Rate Expected',min_value=0.5,max_value=50.0,value=default_values['start_return_rate'],step=0.5,key=3)
            end_return_rate=st.slider('Max Return Rate Expected',min_value=0.5,max_value=50.0,value=default_values['end_return_rate'],step=0.5,key=2)
    else:
        start_rr_str='Return Rate'
        if number_input:
            start_return_rate=st.number_input('Return Rate',min_value=0.5,max_value=50.0,value=default_values['end_return_rate'],step=0.5,key=1)
        else:
            start_return_rate=st.slider('Return Rate',min_value=0.5,max_value=50.0,value=default_values['end_return_rate'],step=0.5,key=1)
        end_return_rate=start_return_rate
    if number_input:
        principal_amount=st.number_input('Monthly SIP Amount',min_value=500,max_value=1000000,value=default_values['principal_amount'],step=500,key=4)
        period=st.number_input('Period',min_value=1,max_value=100,value=default_values['period'],step=1,key=9)
        stop_sip_year=st.number_input('Stop SIP year',min_value=0,max_value=period-1,value=0,step=1,key=16)
        if initial_corpus:
            initial_amount=st.number_input('Initial Amount',min_value=100,max_value=100000000,value=default_values['initial_amount'],step=500,key=5)
        else:
            initial_amount=0
        if step_up:
            if step_up_increment_number:
                default_values['step_up_percentage']=1000
                step_up_percentage=st.number_input('Step Up Rate',min_value=500,max_value=100000,value=int(default_values['step_up_percentage']),step=500,key=6)
            else:
                default_values['step_up_percentage']=10
                step_up_percentage=st.number_input('Step Up Rate',min_value=0.5,max_value=100.0,value=float(default_values['step_up_percentage']),step=0.5,key=6)
            step_up_year=st.number_input('Step Up year',min_value=1,max_value=50,value=default_values['step_up_year'],step=1,key=7)
            step_up_limit=st.number_input('Step Up amount limit',min_value=10000,max_value=1000000,value=default_values['step_up_limit'],step=500,key=8)
        else:
            step_up_percentage=0
            step_up_year=1
            step_up_limit=0
    else:
        principal_amount=st.slider('Monthly SIP Amount',min_value=500,max_value=1000000,value=default_values['principal_amount'],step=500,key=4)
        period=st.slider('Period',min_value=1,max_value=100,value=default_values['period'],step=1,key=9)
        stop_sip_year=st.slider('Stop SIP year',min_value=0,max_value=period-1,value=0,step=1,key=17)
        if initial_corpus:
            initial_amount=st.slider('Initial Amount',min_value=100,max_value=100000000,value=default_values['initial_amount'],step=500,key=5)
        else:
            initial_amount=0
        if step_up:
            if step_up_increment_number:
                default_values['step_up_percentage']=1000
                step_up_percentage=st.slider('Step Up Rate',min_value=500,max_value=100000,value=int(default_values['step_up_percentage']),step=500,key=6)
            else:
                default_values['step_up_percentage']=10
                step_up_percentage=st.slider('Step Up Rate',min_value=0.5,max_value=100.0,value=float(default_values['step_up_percentage']),step=0.5,key=6)
            step_up_year=st.slider('Step Up year',min_value=1,max_value=50,value=default_values['step_up_year'],step=1,key=7)
            step_up_limit=st.slider('Step Up amount limit',min_value=10000,max_value=1000000,value=default_values['step_up_limit'],step=500,key=8)
        else:
            step_up_percentage=0
            step_up_year=1
            step_up_limit=0

default_values={
    'range':range,
    'number_input':number_input,
    'initial_corpus':initial_corpus,
    'step_up':step_up,
    'start_return_rate':start_return_rate,
    'end_return_rate':end_return_rate,
    'principal_amount':principal_amount,
    'period':period,
    'initial_amount':initial_amount,
    'step_up_limit':step_up_limit,
    'step_up_year':step_up_year,
    'step_up_percentage':step_up_percentage,
    'step_up_increment_number':step_up_increment_number
    
    
    
}

if not(initial_corpus):
    initial_amount=0
if not(step_up):
    step_up_percentage=0
    step_up_year=1
    step_up_limit=0



result,yearly_calculations=future_value(principal_amount=principal_amount,calculated_return_rate=range,
                            start_return_rate=start_return_rate,end_return_rate=end_return_rate,
                            initial_amount=initial_amount,period=period,
                            annual_stepup=step_up_percentage,stepup_percentage=not(step_up_increment_number),stepup_everyyear=step_up_year,
                            max_stepup_limit=step_up_limit,stop_year=stop_sip_year,print_result=False)

col1,col2=st.columns([1 ,1])
for i,(k,v) in enumerate(result.items()):
    if i<3:
        col1.markdown(f'> ### **{k}:** *{"₹ {:,}".format(v)}*')
submit=col2.button('Details')
if __name__ == '__main__': 
    if submit:
        result,yearly_calculations=future_value(principal_amount=principal_amount,calculated_return_rate=range,
                            start_return_rate=start_return_rate,end_return_rate=end_return_rate,
                            initial_amount=initial_amount,period=period,
                            annual_stepup=step_up_percentage,stepup_percentage=not(step_up_increment_number),stepup_everyyear=step_up_year,
                            max_stepup_limit=step_up_limit,print_result=False)
        # result,yearly_calculations=future_value(principal_amount=default_values['principal_amount'],calculated_return_rate=default_values['range'],
        #                     start_return_rate=default_values['start_return_rate'],end_return_rate=default_values['end_return_rate'],
        #                     initial_amount=default_values['initial_amount'],period=default_values['period'],
        #                     annual_stepup=default_values['step_up_percentage'],
        #                     stepup_percentage=not(default_values['step_up_increment_number']),stepup_everyyear=default_values['step_up_year'],
        #                     max_stepup_limit=default_values['step_up_limit'],print_result=False)
        result['Base Monthly amount']=principal_amount
        if initial_corpus:
            result['Initial Invested']=initial_amount
        if step_up:
            result['Step Up Percentage %']=step_up_percentage
            result['Step Up every']=f'{str(step_up_year)} year'
            result['Step Up limit']=step_up_limit
        print(result)
        show_result(result,yearly_calculations)


