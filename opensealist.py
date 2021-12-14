import itertools
import os

import pandas
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as ExpectedConditions
import requests

firstRun = True

def retrieveItemList(ownerHash):
    limit = 50
    tokens = {}
    for offset in range(0, 150):
        url = "https://api.opensea.io/api/v1/assets?owner=" + ownerHash + \
              "&order_by=pk" \
              "&order_direction=asc" \
              "&offset=" + str(offset * (limit - 1)) + \
              "&limit=" + str(limit) + \
              "&collection=the-abcs"
        response = requests.request("GET", url)
        jsonResult = response.json()['assets']
        newTokens = {jsonResult[i]['name']: jsonResult[i] for i in range(0, len(jsonResult), 1)}
        tokens = tokens | newTokens
        print('grabbed ', len(jsonResult), 'nfts, token count: ', len(tokens))
    col_name = ["id", "val"]
    with open("nftList.csv", 'w') as f:
        # f.write('sep=,\n')
        for key, val in tokens.items():
            line = str(key) + ',' + str(val['id']) + ',' + str(val['token_id']) + ',' + str(val['permalink']) + '\n'
            # print(line)
            f.write(line)

#lists items from a csv file
def listItems(startItemId, count, isrinkeby, mnemonicString, walletPwd, ownerHash):
    # uncomment to build list of all nfts for owner
    # retrieveItemList(ownerHash)
    # create an object to interact with the Opensea API (need an api key)
    chop = webdriver.ChromeOptions()
    chop.add_extension('MetaMask_v10.0.2.crx')
    driver = webdriver.Opera(options=chop)
    wait = WebDriverWait(driver, 60)
    df = pandas.read_csv('nftList.csv')
    for index, row in df.iterrows():
        itemUrl = row['link'] + '/sell'
        itemId = int(row['itemId'][10:])
        if itemId < startItemId or itemId >= startItemId + count:
            print('skipping row:', index, itemUrl)
            continue
        uploadItem(driver, isrinkeby, itemId, itemUrl, mnemonicString, wait, walletPwd)

#uploads a single item with retry for failure
def uploadItem(driver, isrinkeby, itemId, itemUrl, mnemonicString, wait, walletPwd):
    try:
        global firstRun
        print('Running row:', itemId, itemUrl, firstRun)
        driver.get(itemUrl)
        time.sleep(0.5)
        if firstRun:
            signIntoMeta(driver, wait, isrinkeby, mnemonicString, walletPwd)
        tabs2 = driver.window_handles
        driver.switch_to.window(tabs2[1])
        time.sleep(2)
        firstRun = False
        priceInputXpath = '/html/body/div[1]/div[1]/main/div/div/div[3]/div/div[2]/div/div[1]/form/div[2]/div/div[2]/div[1]/div/div[2]/input'
        wait.until(ExpectedConditions.presence_of_element_located(
            (By.XPATH,
             priceInputXpath)))
        priceInput = driver.find_element_by_xpath(priceInputXpath)
        priceInput.send_keys('0.02')
        listButtonXpath = '/html/body/div[1]/div[1]/main/div/div/div[3]/div/div[2]/div/div[1]/form/div[6]/button'
        wait.until(ExpectedConditions.presence_of_element_located(
            (By.XPATH,
             listButtonXpath)))
        listButton = driver.find_element_by_xpath(listButtonXpath)
        listButton.click()
        wait.until(ExpectedConditions.number_of_windows_to_be(3))
        tabs2 = driver.window_handles
        driver.switch_to.window(tabs2[2])
        signButtonXpath = '/html/body/div[1]/div/div[3]/div/div[3]/button[2]'
        wait.until(ExpectedConditions.presence_of_element_located(
            (By.XPATH,
             signButtonXpath)))
        signButton = driver.find_element_by_xpath(signButtonXpath)
        signButton.click()
        wait.until(ExpectedConditions.number_of_windows_to_be(2))
        driver.switch_to.window(tabs2[1])
        print('completed listing of: ', itemId)
    except Exception as e:
        print(e)
        uploadItem(driver, False, isrinkeby, itemId, itemUrl, mnemonicString, wait, walletPwd)


def signIntoMeta(driver, wait, isrinkeby, mnemonicString, walletPwd):
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[0])
    time.sleep(0.5)
    # driver.close()
    # driver.switch_to.window(tabs2[1])
    button = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button')
    button.click()
    print('meta clicked')
    time.sleep(1)
    button = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button')
    button.click()
    button = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[1]')
    button.click()
    time.sleep(1)
    mnemonicInput = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[1]/div/input')
    mnemonicInput.send_keys(mnemonicString)
    pwd1Input = driver.find_element_by_xpath('//*[@id="password"]')
    pwd1Input.send_keys(walletPwd)
    pwd2Input = driver.find_element_by_xpath('//*[@id="confirm-password"]')
    pwd2Input.send_keys(walletPwd)
    checkbox = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/div')
    checkbox.click()
    submit = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/button')
    submit.click()
    time.sleep(1.5)
    alldone = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/button')
    alldone.click()
    time.sleep(1)
    xmodal = driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button')
    xmodal.click()
    time.sleep(0.01)
    if isrinkeby:
        network = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div')
        network.click()
        time.sleep(0.1)
        networkRinkeby = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/li[4]')
        networkRinkeby.click()
    driver.switch_to.window(tabs2[1])
    time.sleep(0.1)
    oswalleticon = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/nav/ul/div[2]/li/button')
    oswalleticon.click()
    time.sleep(0.2)
    metaicon = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/aside/div[2]/div/div[2]/ul/li[1]/button')
    metaicon.click()
    time.sleep(2)
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[2])
    print(tabs2)
    connectnext = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]')
    connectnext.click()
    time.sleep(1)
    connect = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]')
    connect.click()
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[1])
    print('completed tab sw1')
    driver.switch_to.window(tabs2[2])
    print('completed tab sw2')
    print(tabs2)
    print(driver.title)
    time.sleep(1)
    driver.switch_to.window(tabs2[1])
    walletButtonXpath = '/html/body/div[1]/div[1]/div[1]/nav/ul/div[2]/li/button'
    wait.until(ExpectedConditions.presence_of_element_located(
        (By.XPATH,
         walletButtonXpath)))
    walletButton = driver.find_element_by_xpath(walletButtonXpath)
    walletButton.click()
    print('sign into meta completed')


if __name__ == '__main__':
    listItems(4949, 100, False,
              mnemonicString='',
              walletPwd='',
              ownerHash=''
              )
