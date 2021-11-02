from stock_obj import StockObj
import smtplib
import os
from tick_list import get_tic_list
import pandas as pd

def main():

    answer = []
    tic_list = get_tic_list()
    for tic in tic_list:
        print(tic)
        try:
            x = StockObj(tic)
        except:
            #print(f'bad: {tic}')
            pass
        else:
            if x.spike > 0:
                print(f'good: {tic}')
                answer.append((tic, x.current_price, x.year_return, x.max_revenue, x.average_revenue, x.max_earnings, x.average_earnings, x.sector, x.industry, x.summary ))
    message = pd.DataFrame(answer, columns=['TIC', 'price', '52 Week Return', 'Max Revenue Change',
                                             'Average Revenue Change', 'Max Earnings Change',
                                            'Average Earnings Change', 'Sector', 'Industry', 
                                            'Summary' 
                                            ]
                            )
    message.to_csv('test.csv')   
    send_email(message=message)

def send_email(message):
    mail_address = None #add
    mail_psswd = None #add
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(mail_address, mail_psswd)
        
        smtp.sendmail(mail_address, [None], message) #add

if __name__ == '__main__':
    main()


