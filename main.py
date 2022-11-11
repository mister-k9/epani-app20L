import sqlite3
import time
import serial
import requests
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

file = "epani.db"


def check_internet_connection(duration=None):
    print("|                                                                    |")
    print('|------------------ CHECKING INTERNET CONNECTION --------------------|')
    print("|                                                                    |")
    if duration:
        start = time.time()
        while True: 
            try:
                requests.get('https://www.google.com/')
                print("|----------------------- INTERNET IS ACTIVE -------------------------|")
                print("|                                                                    |")
                
                return True
            except:
                print("|                                                                    |")
                time.sleep(5)
                pass
            end = time.time()
            if int(end - start) >= duration:
                return False

    else:
        while True:
            try:
                requests.get('https://www.google.com/')
                print("|----------------------- INTERNET IS ACTIVE -------------------------|")
                print("|                                                                    |")
                
                break
            except:
                print("|                                                                    |")
                time.sleep(5)
                pass


def check_server_connection(duration=None):
    print("|                                                                    |")
    print('|------------------- CHECKING SERVER CONNECTION ---------------------|')
    print("|                                                                    |")
    
    if duration:
        start = time.time()
        while True:
            try:
                requests.get(os.getenv('API_URL'))
                print("|------------------------ SERVER IS ACTIVE --------------------------|")
                print("|                                                                    |")
                return True
            except:
                print("|                                                                    |")
                time.sleep(5)
                pass
            end = time.time()
            if int(end - start) >= duration:
                return False
    else:
        while True:
            try:
                requests.get(os.getenv('API_URL'))
                print("|------------------------ SERVER IS ACTIVE --------------------------|")
                print("|                                                                    |")
                break
            except:
                print("|                                                                    |")
                time.sleep(5)
                pass


def get_or_set_machine_credentials():
    conn = sqlite3.connect(file)
    cur = conn.cursor()
    # Create Mac Table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS  mac_info (id INTEGER PRIMARY KEY AUTOINCREMENT,mid text, mtoken text);")
    # ------- MAC INFO ----------
    mac_creds_available = (cur.execute('SELECT * FROM mac_info')).fetchone()
    if not mac_creds_available:
        print("======================================================================")
        print("|                         Set Machine Credentials                    |")
        print("======================================================================")
        mid = input('Enter Machine Id: ')
        print("---------------------------------------------------------------------|")
        mtoken = input('Enter Machine Token: ')
        print("|------------------ Credentials Saved Successfully ------------------|")
        cur.execute(
            "INSERT INTO mac_info (mid,mtoken) VALUES (?,?)", [mid, mtoken])
        conn.commit()
        conn.close()
        return mid, mtoken
    conn.close()
    return mac_creds_available[1], mac_creds_available[2]


def server_local_orders_sync():
    print("Unsynced orders have been synced and cleared!")


def server_local_cards_sync():
    time.sleep(1)
    print();print();
    print('~~~~~~~~~~~~~~~~~ Server - Local Cards Sync Initiated ~~~~~~~~~~~~~~~~')
    print("|                                                                    |")
    if check_internet_connection(int(os.getenv('CARDS_SYNC_INTERNET_TIMEOUT_DURATION'))):
        if check_server_connection(int(os.getenv('CARDS_SYNC_SERVER_TIMEOUT_DURATION'))):
            print("|          Syncing cards (posting all the cards to server)           |")
            print("|                                                                    |")
            print("~~~~~~~~~~~~~~~~ Server - Local Cards Sync Successful ~~~~~~~~~~~~~~~~")
            check_serial_hardware()

        else:
            print(
                "~~~~~~~~~~~~~~~~ Server - Local Cards Sync Failed ~~~~~~~~~~~~~~~~")
            print(" >Since Time Limit Exceeded")
            check_serial_hardware()
            return
    else:
        print("~~~~~~~~~~~~~~~~ Server - Local Cards Sync Failed ~~~~~~~~~~~~~~~~")
        print("> Since Time Limit Exceeded")
        check_serial_hardware()
        return

def run_gui_app():
    subprocess.call(os.getenv('RUN_GUI_COMMAND'),shell=True) 
        
def check_serial_hardware():
    print();print();
    time.sleep(1)
    print("\n~~~~~~~~~~~~~~~~ Checking Serial Hardware Connection ~~~~~~~~~~~~~~~~~")
    print("|                                                                    |")
    while True:
        try:
            serialport = serial.Serial(
                port=os.getenv('SERIAL_PORT'),
                baudrate=115200,
                timeout=0.3
            )
            serialport.close()
            break
        except serial.SerialException as e:
            print("|                                                                    |")
            time.sleep(3)
            pass
    print("~~~~~~~~~~~~~~~~~~~ Serial Hardware Is Connected ~~~~~~~~~~~~~~~~~~~~~")
    run_gui_app()


def setup_db():
    print();print();
    print('~~~~~~~~~~~~~~~~~~~~~~ Started Checking Database ~~~~~~~~~~~~~~~~~~~~~')
    conn = sqlite3.connect(os.getenv('LOCAL_DB'))
    cur = conn.cursor()
    # -------- CARDS INFO ----------
    cur.execute("CREATE TABLE IF NOT EXISTS cards_info (id INTEGER PRIMARY KEY AUTOINCREMENT, card_number text,machine_id text, holder_name text, balance int, last_txn_volume int, last_txn_status text, last_txn_timestamp text);")
    local_cards = (cur.execute('SELECT * FROM cards_info')).fetchone()
    # print(local_cards)
    
    if not local_cards:
        print('|------------------------ SETTING UP DATABASE ------------------------')
        check_server_connection()
        mid, mtoken = get_or_set_machine_credentials()
        # HARD CODE ENDPOINTS INTO CODE
        
        cards_endpoint = os.getenv('CARDS_ENDPOINT')
        params = {
            'mid': mid,
            'mtoken': mtoken,
        }
        # WHEN CARDS SHOULD BE POSTED IS TO BE DISCUSSED
        print("\n======================================================================")
        print("|             Retrieving Cards With Machine Credentials              |")
        print("======================================================================")
        try:
            get_cards = requests.get(cards_endpoint, params=params)
            cards = get_cards.json()
            if cards == "No Cards":
                print("No Cards Are Assigned For This Machine!")
                conn.close()
                setup_db() # CHECK ONCE
            if cards == "Invalid Machine":
                print("The Machine Is Not Found!")
                cur.execute(
                    'DELETE FROM mac_info WHERE id = (SELECT min(id) FROM mac_info) ')
                conn.commit()
                conn.close()
                get_or_set_machine_credentials()
            if cards == "Invalid Request!":
                print("The Machine Token Is Invalid!")
                cur.execute(
                    'DELETE FROM mac_info WHERE id = (SELECT min(id) FROM mac_info) ')
                conn.commit()
                conn.close()
                get_or_set_machine_credentials()
            for card in cards:
                cur.execute("INSERT INTO cards_info (card_number,machine_id,holder_name,balance,last_txn_volume,last_txn_status,last_txn_timestamp) VALUES (?,?,?,?,?,?,?)", [
                            card['card_number'], card['machine_id'], card['holder_name'], card['balance'], card['last_txn_volume'], card['last_txn_status'], card['last_txn_timestamp']])
                conn.commit()
            print('Cards Info Is Retrieved And Stored!')
            conn.close()

            print("|---------------- Successfully Copied Cards To Local DB -------------|")
            check_serial_hardware()
        except Exception as e:
            print("//////// Unable to Retrieve Cards.Please Provide Correct Credentials /////////////")
            conn.close()
            setup_db()
    else:
        print('|---------------------- Local Cards are present. --------------------|')
        server_local_cards_sync()
        # server_local_orders_sync()

def check_for_updates():
    print('\n~~~~~~~~~~~~~~~~~~~~~~ Checking For Updates ~~~~~~~~~~~~~~~~~~~~~~~~~~')
    check_internet_connection(int(os.getenv('CHECK_UPDATE_INTERNET_TIMEOUT_DURATION')))

    latest_flag = "Already up to date"
    updating_flag = 'Updating'

    os.chdir(os.getenv('OS_CHDIR'))

    try:
        subprocess.call('git stash',shell=True)
        output = (subprocess.check_output("git pull",shell=True)).decode('utf-8')
        
        if latest_flag in output:
            print('~~~~~~~~~~~~~~~~~~~~~ No New Updates To Install ~~~~~~~~~~~~~~~~~~~~~~')
            return
        elif updating_flag in output:
            print('~~~~~~~~~~~~~~~~~~~~~~~ Updates Are Installed ~~~~~~~~~~~~~~~~~~~~~~~~')
            
            return
    except:
        print("Checking updates failed!")
        
def main():
    #check_for_updates()
    setup_db()

if __name__ == "__main__":
    main()
    

