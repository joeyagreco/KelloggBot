from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import requests
import random
import time
import os
import tempfile, shutil
from faker import Faker
fake = Faker()
chromedriver_location = "./chromedriver"

urls = ['https://jobs.kellogg.com/job/Lancaster-Permanent-Production-Associate-Lancaster-PA-17601/817684800/#',
        'https://jobs.kellogg.com/job/Omaha-Permanent-Production-Associate-Omaha-NE-68103/817685900/z',
        'https://jobs.kellogg.com/job/Battle-Creek-Permanent-Production-Associate-Battle-Creek-MI-49014/817685300/',
        'https://jobs.kellogg.com/job/Memphis-Permanent-Production-Associate-Memphis-TN-38114/817685700/'
        ]


data2 = {
    'resume': '//*[@id="49:_file"]',
    'addy': '//*[@id="69:_txtFld"]',
    'city': '//*[@id="73:_txtFld"]',
    'zip': '//*[@id="81:_txtFld"]',
    'job': '//*[@id="101:_txtFld"]',
    'salary': '//*[@id="172:_txtFld"]',
    'country': '//*[@id="195:_select"]'
}
data = {
    'email': '//*[@id="fbclc_userName"]',
    'email-retype': '//*[@id="fbclc_emailConf"]',
    'pass': '//*[@id="fbclc_pwd"]',
    'pass-retype': '//*[@id="fbclc_pwdConf"]',
    'first_name': '//*[@id="fbclc_fName"]',
    'last_name': '//*[@id="fbclc_lName"]',
    'pn': '//*[@id="fbclc_phoneNumber"]',

}


cities = {'Lancaster':	'Pennsylvania',
          'Omaha':	'Nebraska',
          'Battle Creek':	'Michigan',
          'Memphis':	'Tennessee',
          }

zip_codes = {
    'Lancaster':	['17573', '17601', '17602', '17605', '17606', '17699'],
    'Omaha':	['68104', '68105', '68106', '68124', '68127', '68134'],
    'Battle Creek':	['49014', '49015', '49016', '49017', '49018', '49037'],
    'Memphis':	['38116', '38118', '38122', '38127', '38134', '38103'],
}


gender = ['Male', 'Female', 'Other']





class JobApp():
    def __init__(self):
        self.opt = Options()
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(chromedriver_location, options=self.opt)
        self.driver.minimize_window()
        self.status = True
        self.gender = random.choice(gender)
        self.email = fake.free_email()
        self.password = fake.password()
        
        
    def get_urls(self):
        self.j = random.randint(0, 3)
        try:
            self.driver.get(urls[self.j])
            self.driver.implicitly_wait(10)
        except Exception as e:
            print("failed 1: " + str(e))
            self.status = False

    def click_apply(self):
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[2]/div/div[1]/div[1]/div/div/button').click()
        self.driver.find_element_by_xpath(
            '//*[@id="applyOption-top-manual"]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="page_content"]/div[2]/div/div/div[2]/div/div/div[2]/a').click()

    def create_account(self):
        for key in data.keys():
            if key == 'email':
                info = self.email
            if key == 'email-retype':
                info = self.email
            if key == 'pass':
                info = self.password
            if key == 'pass-retype':
                info = self.password
            if key == 'first_name':
                info = fake.first_name()
                self.first_name = info
            if key == 'last_name':
                info = fake.last_name()
                self.last_name = info
            if key == 'pn':
                info = fake.phone_number()

            try:
                self.driver.find_element_by_xpath(data.get(key)).send_keys(info)
            except:
                print("Failed to enter account data")
                self.status = False


        try:
            time.sleep(random.randint(0, 2))
            select = Select(self.driver.find_element_by_id('fbclc_ituCode'))
            select.select_by_value('US')
            select = Select(self.driver.find_element_by_id('fbclc_country'))
            select.select_by_value('US')




            self.driver.find_element_by_xpath('//*[@id="dataPrivacyId"]').click()
            time.sleep(1.5)
            self.driver.find_element_by_xpath('//*[@id="dlgButton_20:"]').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '//*[@id="fbclc_createAccountButton"]').click()

            time.sleep(1.5)
        except:
            print("Failed to create account")
            self.status = False

    
    def fill_application(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//*[@id="109:topBar"]').click()
        self.driver.find_element_by_xpath('//*[@id="260:topBar"]').click()

        if self.j == 0:
            city = 'Lancaster'
        elif self.j == 1:
            city = 'Omaha'
        elif self.j == 2:
            city = 'Battle Creek'
        elif self.j == 3:
            city = 'Memphis'

        num = random.randint(0, 5)

        for key in data2.keys():

            if key == 'resume':
                self.driver.find_element_by_xpath(
                    '//*[@id="48:_attach"]/div[6]').click()

                info = self.rename_resume(os.getcwd()+"/src/resume.png")
            if key == 'addy':
                info = fake.street_address()
            if key == 'city':
                info = city
                self.city = city
            if key == 'zip':
                zipp = zip_codes[city]
                info = zipp[num]
            if key == 'job':
                info = fake.job()
            if key == 'salary':
                info = random.randint(15, 35)

            try:
                self.driver.find_element_by_xpath(data2.get(key)).send_keys(info)
            except Exception as e:
                print("failed 2: " + str(e))
                self.status = False

        try:
            select = Select(self.driver.find_element_by_id('154:_select'))
            select.select_by_visible_text('Yes')
            select = Select(self.driver.find_element_by_id('195:_select'))
            select.select_by_visible_text('United States')

            select = Select(self.driver.find_element_by_id('211:_select'))
            select.select_by_visible_text('Yes')
            select = Select(self.driver.find_element_by_id('215:_select'))
            select.select_by_visible_text('No')
            select = Select(self.driver.find_element_by_id('219:_select'))
            select.select_by_visible_text('No')
            select = Select(self.driver.find_element_by_id('223:_select'))
            select.select_by_visible_text('No')
            select = Select(self.driver.find_element_by_id('227:_select'))
            select.select_by_visible_text('No')
            select = Select(self.driver.find_element_by_id('231:_select'))
            select.select_by_visible_text('Yes')
            select = Select(self.driver.find_element_by_id('223:_select'))
            select.select_by_visible_text('No')

            time.sleep(1)
            
            select = Select(self.driver.find_element_by_id('235:_select'))
            
            select.select_by_visible_text(self.gender)

            self.driver.find_element_by_xpath('//label[text()="350 LBS"]').click()
            self.driver.find_element_by_xpath('//label[text()="800 LBS"]').click()
            els = self.driver.find_elements_by_xpath('//label[text()="Yes"]')
            for el in els:
                el.click()

            time.sleep(5)
            self.driver.find_element_by_xpath('//*[@id="261:_submitBtn"]').click()
        except:
            pass

    def rename_resume(self, path):
        temp_dir = tempfile.gettempdir()
        self.temp_path = os.path.join(temp_dir, 'resume_' + self.first_name + '_' + self.last_name + '.png')
        shutil.copy2(path, self.temp_path)
        return self.temp_path

    def close_window(self):
        os.remove(self.temp_path)
        self.driver.close()

    def apply(self):
        self.get_urls()
        if self.status == True:
            self.click_apply()
        if self.status == True:
            self.create_account()
        if self.status == True:
            self.fill_application()

        self.close_window()
        return self.city, self.gender, self.first_name, self.last_name, self.email