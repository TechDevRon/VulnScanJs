from colored import Fore, Back, Style
import threading
import requests
from requests.exceptions import Timeout
import argparse
import re
import queue
import os
import sys

banner = f"""{Back.rgb('160', '32', '240')}
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓███████▓▒░  ░▒▓███████▓▒░ ░▒▓██████▓▒░  ░▒▓██████▓▒░ ░▒▓███████▓▒░        ░▒▓█▓▒░ ░▒▓███████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░        
 ░▒▓█▓▒▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░        
 ░▒▓█▓▒▒▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓██████▓▒░ ░▒▓█▓▒░       ░▒▓████████▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░ ░▒▓██████▓▒░  
  ░▒▓█▓▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░ 
  ░▒▓█▓▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒░ 
   ░▒▓██▓▒░    ░▒▓██████▓▒░ ░▒▓████████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░  ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓██████▓▒░ ░▒▓███████▓▒░{Style.reset}
"""
print(banner)

urls_list = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

output_queue = queue.Queue()

def initialize(urls_file, wordlist_file):

    wordlist_data = []

    try:
        if wordlist_file:
            with open(wordlist_file, 'r') as word_file:
                for line in word_file:
                    wordlist_data.append(line.strip())

        else:

            for line in sys.stdin:
                wordlist_data.append(line.strip().encode('utf-8'))

    except Exception as e:

        print(f'{Fore.red}{e}{Style.reset}')

    try:
        
        with open(urls_file, 'r') as url_file:
            for url in url_file:
                urls_list.append(url.strip())
        return wordlist_data

    except Exception as e:

        print(f'{Fore.red}{e}{Style.reset}')
        os._exit(1)


def perform_scan(url, wordlist_data, timeout, defaultmatching):

    output = [] 
    
    output.append(f"\n\n{Fore.blue}[*]Target:{Style.reset}{Fore.rgb('255', '165', '0')} {url}{Style.reset}")
    output.append(f"{Fore.blue}[*]Loading{Style.reset}")
    
    try:
        output.append(f"{Fore.blue}[*]Connecting...{Style.reset}")
        response = requests.get(url, headers=headers, timeout=timeout)
        output.append(f"{Fore.blue}[*]Connected/status: {response.status_code}{Style.reset}\n")
    
    except requests.exceptions.RequestException as e:
        output.append(f"{Fore.red}Error: {e}{Style.reset}")
        output_queue.put('\n'.join(output)) 
        os._exit(1)

    except KeyboardInterrupt as k:
        print("{Fore.red}Error: {e}")
        print(f"Keyboard Interruption Exiting.....{Style.reset}")
        os._exit(1)

    if not wordlist_data:
        output.append(f"{Fore.red}Wordlist empty.{Style.reset}")
        output_queue.put('\n'.join(output))  
        return

    if defaultmatching  == True:

        for word in wordlist_data:

            matches = re.findall(rf'\b{re.escape(word)}\b', response.text)
            if matches:
                output.append(f"{Fore.green}[Found] Keyword '{word}': Found {len(matches)} matches{Style.reset}")

    elif defaultmatching == False:

        for word in wordlist_data:

            rword = re.compile(word.strip())
            matches = re.findall(rword, response.text)

            if matches:
                output.append(f"{Fore.green}[Found] Keyword '{word}': Found {len(matches)} matches{Style.reset}")

        output.append("\n")
        response.close()
    
    output_queue.put('\n'.join(output))

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Js Scanner")
    parser.add_argument('-u', '--urls', type=str, help='File containing urls.')
    parser.add_argument('-w', '--wordlist', type=str, default='default/defaultWordlist', help='File of js functions to look for ex: eval. each word on different line.')
    parser.add_argument('-t', '--timeout', type=int, default='15', help='Request time out length.')
    parser.add_argument('-m', '--matching', default=False, action='store_true',help='This opinion enables defualt matching meaning no regex in file, note you could put regex in the word list file and it will compile if opinion isn\'t used.')

    threads = []
    arguments = parser.parse_args()
    wordlist = initialize(arguments.urls, arguments.wordlist)

    print(f"{Fore.blue}[*]Starting...") 
    print(f"[*]Adding threads...")

    for url in urls_list:
        thread = threading.Thread(target=perform_scan, args=(url, wordlist, arguments.timeout, arguments.matching))
        threads.append(thread)
    
    print("[*]Starting threads...")
    print("[*]Connecting to sites, and scanning js, please be patience...")

    for thread in threads:
        thread.start()
    
    print(f"[*]Joining threads...{Style.reset}\n\n")

    for thread in threads:
        thread.join()  

    while not output_queue.empty():
        print(output_queue.get())
