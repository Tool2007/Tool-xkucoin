import time
import requests
import random
import urllib.parse
import os
import signal
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama for color output
init(autoreset=True)

# Global variable to control the main loop
running = True

def signal_handler(signum, frame):
    global running
    running = False
    print(Fore.LIGHTBLACK_EX + f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.YELLOW + "Đã nhận được tín hiệu tư sever. Đang chuẩn bị vào tool...")

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def art(total_accounts):
    print(Fore.GREEN + Style.BRIGHT + r"""
   
   ____                            _______ _      __         _     
  / __ \                          |__   __| |     \_\       | |    
 | |  | |_   _  __ _ _ __   __ _     | |  | |__   __ _ _ __ | |__  
 | |  | | | | |/ _` | '_ \ / _` |    | |  | '_ \ / _` | '_ \| '_ \ 
 | |__| | |_| | (_| | | | | (_| |    | |  | | | | (_| | | | | | | |
  \___\_\\__,_|\__,_|_| |_|\__, |    |_|  |_| |_|\__,_|_| |_|_| |_|
                            __/ |                                  
                           |___/                                   

                                                                
    Auto Claim Bot For XkuCoin 
    Admin : Quang Thành Coder 👨‍💻
    """ + Style.RESET_ALL)
    
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tài khoản: {total_accounts}")
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts

def decode_data(encoded_data):
    params = dict(item.split('=') for item in encoded_data.split('&'))

    decoded_user = urllib.parse.unquote(params['user'])
    decoded_start_param = urllib.parse.unquote(params['start_param'])

    return {
        "decoded_user": decoded_user,
        "decoded_start_param": decoded_start_param,
        "hash": params['hash'],
        "auth_date": params['auth_date'],
        "chat_type": params['chat_type'],
        "chat_instance": params['chat_instance']
    }

def login(decoded_data):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/login?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3"
    }
    
    body = {
        "inviterUserId": "5496274031",
        "extInfo": {
            "hash": decoded_data['hash'],
            "auth_date": decoded_data['auth_date'],
            "via": "miniApp",
            "user": decoded_data['decoded_user'],
            "chat_type": decoded_data['chat_type'],
            "chat_instance": decoded_data['chat_instance'],
            "start_param": decoded_data['decoded_start_param']
        }
    }

    session = requests.Session()
    response = session.post(url, headers=headers, json=body)
    cookie = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])             
    return cookie

def data(cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    balance = data.get("data", {}).get("availableAmount")
    molecule = data.get("data", {}).get("feedPreview", {}).get("molecule")
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.GREEN + f"Số dư: " + Fore.WHITE + f"{balance}")
    return molecule

def tap(cookie, molecule):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/gold/increase?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }

    total_increment = 0

    while total_increment < 3000 and running:
        increment = random.randint(55, 60)
        form_data = {
            'increment': str(increment),
            'molecule': str(molecule)
        }

        try:
            response = requests.post(url, headers=headers, data=form_data)
            total_increment += increment
            
            print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                  Fore.GREEN + f"Tap: " + Fore.WHITE + f"{increment} | " + 
                  Fore.GREEN + f"Tổng số lần Tap: " + Fore.WHITE + f"{total_increment}/3000")
            
            time.sleep(2)
        except requests.exceptions.RequestException:
            print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                  Fore.RED + "Đã xảy ra lỗi mạng. Đang thử lại...")
            time.sleep(5)

def new_balance(cookie):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"111\", \"Not(A:Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-request-with": "null",
        "Referer": "https://www.kucoin.com/miniapp/tap-game?inviterUserId=5496274031&rcode=QBSTAPN3",
        "cookie": cookie
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    balance = data.get("data", {}).get("availableAmount")
    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
          Fore.GREEN + f"Số dư mới: " + Fore.WHITE + f"{balance}")

def main():
    global running
    file_path = "data.txt"
    encoded_data_list = read_data_file(file_path)
    total_accounts = len(encoded_data_list)
    
    try:
        while running:
            clear_terminal()
            art(total_accounts)
        
            for index, encoded_data in enumerate(encoded_data_list, start=1):
                if not running:
                    break
                print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                      Fore.GREEN + f"Đang xử lý số tài khoản.{index}")
                try:
                    decoded_data = decode_data(encoded_data)
                    cookie = login(decoded_data)
                    molecule = data(cookie)
                    tap(cookie, molecule)
                    new_balance(cookie)
                except Exception as e:
                    print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                          Fore.RED + f"Lỗi xử lý tài khoản {index}: {str(e)}")
            
            if running:
                print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
                      Fore.YELLOW + "Chờ 2 phút trước vòng lặp tiếp theo...")
                for _ in range(120):
                    if not running:
                        break
                    time.sleep(1)
    except Exception as e:
        print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
              Fore.RED + f"Đã xảy ra lỗi không mong muốn: {str(e)}")
    finally:
        print(Fore.LIGHTBLACK_EX + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " + 
              Fore.GREEN + "Đã đăng xuất thành công khỏi bot. Tạm biệt!")

if __name__ == "__main__":
    main()
