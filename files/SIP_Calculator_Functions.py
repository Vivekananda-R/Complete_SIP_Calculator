import streamlit as st
import random
# import locale
import xlsxwriter
import pandas as pd
from io import BytesIO,StringIO

def future_value(principal_amount=1000,start_return_rate=5,end_return_rate=8,calculated_return_rate=True,initial_amount=0,period=10,
                    annual_stepup=10,stepup_percentage=False,stepup_everyyear=1,max_stepup_limit=50000,stop_year=0,print_result=False):


    if start_return_rate is None or start_return_rate<=0:
        print('Provide a valid start return rate')
        return None
    if end_return_rate is None:
        end_return_rate=start_return_rate
    elif end_return_rate<=0:
        end_return_rate=start_return_rate
        
    print('Start Return Rate:',start_return_rate)
    print('End Return Rate:',end_return_rate)
    if calculated_return_rate:
        average_calculated_cagr=(start_return_rate+end_return_rate)/2
        standard_deviation=(end_return_rate-start_return_rate)/4
        print('Average Return Percentage:',average_calculated_cagr)
        print('Standard Deviation:',standard_deviation)
        random_cagr=round(random.normalvariate(average_calculated_cagr,standard_deviation),2)
        print('Expected CAGR:',random_cagr,'%')
        return_rate=random_cagr
    else:
        return_rate=start_return_rate

    if annual_stepup>=1 and annual_stepup<100:
        annual_stepup=annual_stepup/100
    if return_rate>=1 and return_rate<100:
        return_rate=return_rate/100
    amount_ason_year=[]
    amount_invested=present_amount=initial_amount if initial_amount>0 else 0
    print('Initial Investment:',amount_invested)
    print('Monthly Investment:',principal_amount)
    print('Period:',period,'years')
    print('Return Rate:',return_rate*100,'%')
    print('Annual Step Up percentage:',annual_stepup*100)
    print(f'Step Up every {stepup_everyyear} year:')
    print('Max Step Up amount:',max_stepup_limit)
    print('Stop SIP year:',stop_year)
    if print_result:
        print('Number of iteration M*Y',period*12)
    for i in range((period*12)):
        if print_result:
            print('Y:',(i//12)+1,' M:',(i%12)+1)
            print('Max Stepup Limit:',max_stepup_limit)
            print('Current Amount:',round(present_amount,2))
            print('Monthly Amount:',round(principal_amount,2))
            print('Monthly Return Rate:',(return_rate/12),'%')
            
        present_amount=(round(present_amount,2)+round(principal_amount,2))*((1+(return_rate/12))**(1))
        amount_invested=principal_amount+amount_invested
        if print_result:
            print('Amount invested:',round(amount_invested,2))
            print('After the month amount:',round(present_amount,2))
            print('-'*30)
        if (i+1)%12==0:
            amount_ason_year.append({'Year':(i//12)+1,'Corpus':round(present_amount,2),
                                    'Amount Invested':round(amount_invested,2),
                                    'Monthly Investment':round(principal_amount,2),
                                    'Gain':round(present_amount-amount_invested,2),
                                    'CAGR %':round(return_rate*100,2),
                                    'Annual Step Up %':round(annual_stepup*100,2)})
            if (i//12)+1==stop_year:
                principal_amount=0
                continue
            if (stepup_everyyear>0) and (((i//12)+1)>0) and (((i//12)+1)%stepup_everyyear==0):
                if print_result:
                    print('Entered principal calculator')
                if stepup_percentage:
                    principal_amount=round(principal_amount,2)+round(round(principal_amount,2)*annual_stepup,2)
                else:
                    principal_amount=round(round(principal_amount,2)+annual_stepup,2)
                # principal_amount=round(principal_amount,2)+round(round(principal_amount,2)*annual_stepup,2)
            if principal_amount>=max_stepup_limit and max_stepup_limit>0:
                if print_result:
                    print('Entered max','-'*30)
                principal_amount=max_stepup_limit                                              
    print('Final Value:',round(present_amount,2))
    result={
        
        'Invested':round(amount_invested),
        'Gain':round(present_amount-amount_invested),
        'Total Value':round(present_amount),
        'Return %':round(return_rate*100,2),
        'Period':period,
    }
    return (result,amount_ason_year)

def convert_to_currency_str(items,convert_list=['Invested','Gain','Total Value','Base Monthly amount','Initial Invested','Step Up limit']):
    temp_dict={}
    # locale.setlocale(locale.LC_ALL,'en_IN')
    # locale.setlocale(locale.LC_MONETARY,'en_IN') 
    for k,v in items.items():
        print(k,v)
        if k in convert_list:
            # temp_dict[k]=locale.currency(v,grouping=True).split('.')[0]
            temp_dict[k]='₹ {:,}'.format(v)
        else:
            temp_dict[k]=v
    return temp_dict

@st.cache_resource(show_spinner=False)
def to_excel(df,pf):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    pf.to_excel(writer,index=False,sheet_name='SIP Configs')
    df.to_excel(writer, index=False, sheet_name='SIP Calculation')
    
    writer.close()
    processed_data = output.getvalue()
    return processed_data
   
@st.dialog("SIP Result")
def show_result(items,calculations,separator=': '):
    
    format_items=convert_to_currency_str(items)
    for k,v in format_items.items():
        st.markdown(f'{k}{separator}{v}')
    
    st.download_button(
                label="Download data",
                data=to_excel(pd.DataFrame(calculations),pd.DataFrame([{'Name':k,'Value':v} for k,v in items.items()])),
                file_name=f"SIP_Calculation_{str(items['Base Monthly amount'])}_{str(items['Return %'])}_{str(items['Period'])}.xlsx",
                mime="application/vnd.ms-excel",
            )

    