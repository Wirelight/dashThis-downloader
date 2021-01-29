#! python3
#  dashThisDownload.py - Export PDF files from DashThis dashboards.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, os

#Get DashThis login details
username=input('Provide Username:\n')
password=input('Provide Password:\n')

#Read Text File Into List
clientList=[line.split() for line in open('clientList.txt')]

#List of finished downloads
finishedDownloads=[]

#Core Function
def dashThisDownload(start, end):

    #Initialise Browser
    browser=webdriver.Chrome()
    #Navigate to DashThis and Login
    browser.get('https://dashthis.com/app/admin/Account/Index')
    userElem = browser.find_element_by_id('Email')
    userElem.send_keys(username)
    passElem = browser.find_element_by_id('Password')
    passElem.send_keys(password)
    passElem.submit()
    time.sleep(10)

    #Iterate over each set of dashboards
    for i in range(start, end+1):

        dashboard=clientList[i][0]
        startPeriod=int(clientList[i][1])
        endPeriod=int(clientList[i][2])
        period=startPeriod
        currentClient=''

        #Start Dashboard Loop
        while period < endPeriod+1:

            #Navigate to dashboard and wait for load
            browser.get(f'{dashboard}?period={str(period)}')
            print('Waiting for page load.')
            time.sleep(30)
            print('Finished page load wait.\n')

            #Create Client info
            if period == startPeriod:
                clientName=browser.find_element_by_id('editableTitle').get_attribute('value')
                currentClient=clientName.strip().title()
                if clientName.endswith(' '):
                    clientFileName='+'.join(clientName.split()) + '+.pdf'
                else:
                    clientFileName='+'.join(clientName.split()) + '.pdf'
                clientDirectory=os.path.join('/Users/Giorgio/Downloads/DashThis Reports', currentClient)
                if not os.path.exists(clientDirectory):
                    os.mkdir(clientDirectory)
                    print(f'Making folder: {clientDirectory}.\n')
            clientFileDate=browser.find_element_by_xpath('//*[@id="dashboardHeader"]/div/div[3]/div/div/input').get_attribute('value')
            finalFileName=currentClient + ' - ' + clientFileDate + '.pdf'

            #Find Share Button and Click
            browser.find_element_by_class_name('e2e_sharing_options_button').click()

            #Find Export Button and Click
            browser.find_element_by_xpath('//*[@id="portal-menu"]/div/div/div/div/div/ul/li[3]').click()
            #time.sleep(5)

            #Wait for download to complete
            print(f'{currentClient} - {clientFileDate} PDF export in progress...')
            while not os.path.exists(os.path.join('..', clientFileName)):
                time.sleep(5)
            if os.path.isfile(os.path.join('..', clientFileName)):
                print(f'{currentClient} PDF Export Complete.\n')

            #Find file in download directory, rename and move to client directory
            os.rename(os.path.join('..', clientFileName), os.path.join(clientDirectory, finalFileName))

            #Increase period
            period+=1

        finishedDownloads.append(currentClient)
        print(f'{currentClient} Report Downloads Complete.\n')

dashThisDownload(1, 50)

print('Program Complete. Client Dashboards Exported For:\n')
for i in range(len(finishedDownloads)):
    print(f'  - {finishedDownloads[i]}')
