from selenium import webdriver
import time
import yaml
from urllib.parse import urlparse, parse_qs
import os
import requests

class Workday:
    def __init__(self):
        self.curr_dir = os.path.dirname(os.path.realpath(__file__))

        conf = yaml.load(open(self.curr_dir + '/config.yml'), Loader=yaml.FullLoader)
        self.user = conf['login']
        self.password = conf['password']
        self.login_url = conf['login_url']
        self.api_server_url = conf['server_url']

        with open(self.curr_dir + '/token.txt', "r") as token_file:
            self.headers = {"Authorization": "Bearer " + token_file.read()}
            self.token = token_file.read()


    def get_new_access_token(self):
        driver = webdriver.Chrome(executable_path = self.curr_dir + '\chromedriver.exe')

        driver.get(self.login_url)
        time.sleep(2)

        driver.find_element_by_xpath("//input[@type='text']").send_keys(self.user)
        driver.find_element_by_xpath("//input[@type='password']").send_keys(self.password)
        driver.find_element_by_xpath("//button[@data-automation-id='goButton']").click()
        time.sleep(2)

        driver.find_element_by_xpath("//button[@data-automation-id='linkButton']").click()
        time.sleep(2)

        current_url = driver.current_url
        driver.quit()

        parsed = urlparse(current_url)
        return parse_qs(parsed.fragment)['access_token'][0]

    def refresh_token(self):
        self.token = self.get_new_access_token()
        self.headers = {"Authorization": "Bearer " + self.token}

        with open(self.curr_dir + '/token.txt', "w") as token_file:
            token_file.write(self.token)


    def call_api(self, query: str, method: str):
        if method == 'get' or method == 'GET':
            response = requests.get(self.api_server_url + query, headers=self.headers)
        elif method == 'post' or method == 'POST':
            response = requests.post(self.api_server_url + query, headers=self.headers)
        elif method == 'patch' or method == 'PATCH':
            response = requests.patch(self.api_server_url + query, headers=self.headers)
        else:
            return "Only get, post and patch methods are allowed"

        if response.status_code != 401:
            return response.json()
        else:
            self.refresh_token()
            return self.call_api(query=query, method=method)

    @staticmethod
    def get_access_token():
        curr_dir = os.path.dirname(os.path.realpath(__file__))

        conf = yaml.load(open(curr_dir + '/config.yml'), Loader=yaml.FullLoader)
        user = conf['login']
        password = conf['password']
        login_url = conf['login_url']
        api_server_url = conf['server_url']

        with open(curr_dir + '/token.txt', "r") as token_file:
            token = token_file.read()
            headers = {"Authorization": "Bearer " + token}

        response = requests.get(api_server_url + '/workers/a9aaf0a691fc01f566d2e6f4d80f865a', headers=headers)
        
        if response.status_code != 401:
            return token

        url = "https://impl.workday.com/wday/authgwy/rockwellautomation1/authorize?response_type=token&client_id=NjJlZjk0NmItMzExYy00ZjEwLWEyNTMtZTkyMTNlODRhZTM1"
        driver = webdriver.Chrome(executable_path=curr_dir + '\chromedriver.exe')

        driver.get(url)
        time.sleep(2)

        driver.find_element_by_xpath("//input[@type='text']").send_keys(user)
        driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_xpath("//button[@data-automation-id='goButton']").click()
        time.sleep(2)

        driver.find_element_by_xpath("//button[@data-automation-id='linkButton']").click()
        time.sleep(2)

        current_url = driver.current_url
        driver.quit()

        parsed = urlparse(current_url)
        token = parse_qs(parsed.fragment)['access_token'][0]

        with open(curr_dir + '/token.txt', "w") as token_file:
                token_file.write(token)

        return token
