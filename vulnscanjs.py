from colored import Fore, Back, Style
import requests
import argparse
import re

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

def initialize(urls_file, wordlist_file):
    wordlist_data = []
    
    with open(wordlist_file, 'r') as word_file:
        for line in word_file:
            wordlist_data.append(line.strip())
    
    with open(urls_file, 'r') as url_file:
        for url in url_file:
            urls_list.append(url.strip())
    return wordlist_data

def perform_scan(url, wordlist_data):
    print(f"{Fore.blue}[*]Target:{Style.reset}{Fore.rgb('255', '165', '0')} {url}{Style.reset}\n{Fore.blue}[*]Loading{Style.reset}")
    try:
        print(f"{Fore.blue}[*]Connecting...{Style.reset}")
        response = requests.get(url)
        print(f"{Fore.blue}[*]Connected/status: {response.status_code}{Style.reset}\n")
    
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if not wordlist_data:
        print(f"{Fore.red}Wordlist empty.{Style.reset}")
        return
    
    for word in wordlist_data:
        matches = re.findall(word, response.text)
        
        if matches:
            print(f"{Fore.green}[Found] Keyword '{word}': Found {len(matches)} matches{Style.reset}")
    
    print("\n")
    response.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Js Scanner")
    parser.add_argument('-u', '--urls', type=str, help='File containing urls.')
    parser.add_argument('-w', '--wordlist', type=str, default='default/defaultWordlist', help='File of js functions to look for ex: eval. each word on different line.')

    arguments = parser.parse_args()
    wordlist = initialize(arguments.urls, arguments.wordlist)
    
    for index, url in enumerate(urls_list):
        print(f"{Fore.blue}Scanning URL {index+1}/{len(urls_list)}: {url}{Style.reset}")
        perform_scan(url, wordlist)
