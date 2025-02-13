import streamlit as st
import random
import locale

def future_value(principal_amount=1000,start_return_rate=5,end_return_rate=8,calculated_return_rate=True,initial_amount=0,period=10,
                    annual_stepup=10,stepup_everyyear=1,max_stepup_limit=50000,print_result=False):


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
            
            if (stepup_everyyear>0) and (((i//12)+1)>0) and (((i//12)+1)%stepup_everyyear==0):
                if print_result:
                    print('Entered principal calculator')
                principal_amount=round(principal_amount,2)+round(round(principal_amount,2)*annual_stepup,2)
            if principal_amount>=max_stepup_limit and max_stepup_limit>0:
                if print_result:
                    print('Entered max','-'*30)
                principal_amount=max_stepup_limit                                              
    print('Final Value:',round(present_amount,2))
    result={
        'Invested':round(amount_invested),
        'Return %':round(return_rate*100,2),
        'Period':period,
        'Gain':round(present_amount-amount_invested),
        'Total Value':round(present_amount)
    }
    return (result,amount_ason_year)

def convert_to_currency_str(items,convert_list=['Invested','Gain','Total Value']):
    temp_dict={}
    locale.setlocale(locale.LC_MONETARY,'en_IN') 
    for k,v in items.items():
        if k in convert_list:
            temp_dict[k]=locale.currency(v,grouping=True).split('.')[0]
        else:
            temp_dict[k]=v
    return temp_dict
            
@st.dialog("SIP Result")
def show_result(items,separator=': '):
    for k,v in items.items():
        st.markdown(f'{k}{separator}{v}')
    