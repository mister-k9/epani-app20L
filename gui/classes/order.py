import sqlite3
from datetime import datetime
import requests
from random import randint

import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('/home/pi/Documents/epani-test/.env')
load_dotenv(dotenv_path=dotenv_path)


class Order():
    def __init__(self):
        self.volume = ''
        self.amount = 0
        self.tap = ''
        self.cardNo = ''
        self.dispensed_volume = ''
        self.available_balance = ''
        self.holder_name = ''
        self.internet_available = False
        self.check_internet_connection()

    def check_internet_connection(self):
        if requests.get('https://www.google.com/'):
            self.internet_available = True
        else:
            self.internet_available = False

    def get_tap(self):
        return self.tap

    def get_volume(self):
        return self.volume

    def get_amount(self):
        return self.amount

    def set_tap(self, tap):
        self.tap = tap

    def set_volume(self, volume=0, amount=0):
        self.volume += volume
        self.amount += amount

    def set_cardno(self, card_no=''):
        self.cardNo = card_no

    def process_payment(self):
        if not self.internet_available:

            conn = sqlite3.connect()

            cur = conn.cursor()
            query = 'SELECT name,balance FROM cards_info WHERE card_number =\'' + self.cardNo + "\'"
            cur.execute(query)
            tst = cur.fetchmany()[0]

            current_balance = tst[1]
            card_owner = tst[0]

            if current_balance >= self.amount:
                final_balance = current_balance - self.amount
                nw = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute('UPDATE cards_info SET balance=' + str(final_balance) + ',last_txn_volume=' + str(
                    self.amount) + ',last_txn_timestamp=\'' + nw + "\'" + ' WHERE card_number =\'' + self.cardNo + "\'")
                status = "completed"
                conn.execute('INSERT INTO orders_info (order_id,card_number,volume,amount,txn_status,timestamp) VALUES (?,?,?,?,?,?)', [
                             "orderid", self.cardNo, self.volume, self.amount, status, nw])
                conn.commit()
                self.available_balance = final_balance
                self.holder_name = card_owner
                print(card_owner, current_balance, final_balance)
                conn.close()
                return "payment_done"
            else:
                conn.close()
                return "insufficienct_balance"

        else:
            return self.internet_available_func()

    def is_volume_set(self):
        return self.volume != '' and self.amount != 0

    def is_card_set(self):
        return self.cardNo != ''

    def is_tap_set(self):
        return self.tap != ''

    def print_all(self):
        print("Volume:", self.volume)
        print("Amount:", self.amount)
        print("Card No:", self.cardNo)
        print("Tap:", self.tap)

    def internet_available_func(self):
        try:
            # TODO: IF NOT API WORKING SHOULD NOT GO TO TAP SELECTION, SHOW ERROR
            # TODO: CARD NOT FOUND MESSAGE
            # TODO: NO BALANCE MESSAGE
            # auth_endpoint = "http://localhost:8000/api/auth/"
            # auth_resp = requests.post(auth_endpoint, json={"username": "machine1", "password": "k9k9k9k9"})

            # if auth_resp.status_code == 200:
            #     token = auth_resp.json()['token']

            conn = sqlite3.connect(os.getenv('LOCAL_DB'))
            cur = conn.cursor()
            creds = (cur.execute('SELECT * FROM mac_info')).fetchone()
            conn.close()
            mid, mtoken = creds[1], creds[2]

            deduct_card_balance_endpoint = os.getenv('DEDUCT_CARD_BALANCE_ENDPOINT')
            nw = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                'mid': mid,
                'mtoken': mtoken,
                'volume_in_ml': f'{self.volume}',
                'cno': self.cardNo,
                'am': self.amount,
                'txn_ts': nw,
            }
           
            res = (requests.post(deduct_card_balance_endpoint,json=data)).json()
            if not type(res) == dict:
                if res == 'Invalid Machine':
                    return 'invalid_machine'
                elif res == 'Invalid Request!':
                    return 'invalid_token'
                elif res == 'Invalid Card':
                    return 'card_not_found'

            print(res)
            self.available_balance = res['balance']
            self.holder_name = res['name']
            order_created = res['order_created']

            if not order_created:
                return 'insufficienct_balance'

            return 'payment_done'

            
                

            # order_id = last order id  + 1

            # params = {
            #     'mid': mid,
            #     'mtoken': mtoken
            # }
            # data = {
            #     'card_number': f'{self.cardNo}',
            #     'order_status': 'DONE_PAYMENT',
            #     'amount': f'{self.amount}',
            #     'volume_in_ml': f'{self.volume}',
            #     'local_timestamp': f'{nw}',
            # }
            # post_order_endpoint = os.getenv('CREATE_ORDER_ENDPOINT')
            # post_order = requests.post(
            #     post_order_endpoint, json=data, params=params)
            # res = post_order.json()
            # if res == 'Successful!':
            #     return 'payment_done'
            # elif res == 'Invalid Request!':
            #     return 'invalid_token'
            # elif res == 'Invalid Machine':
            #     return 'invalid_machine'

        except Exception as e:
            print(e)
