import itertools
import os
#unused
import pandas
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as ExpectedConditions


def uploadFiles(startItemId, count, isrinkeby, mnemonicString, walletPwd):
    chop = webdriver.ChromeOptions()
    chop.add_extension('MetaMask_v10.0.2.crx')
    driver = webdriver.Opera(options=chop)
    wait = WebDriverWait(driver, 60)
    df = pandas.read_csv('Generated/metadata.csv')
    if isrinkeby:
        url = 'https://testnets.opensea.io/asset/create'
    else:
        url = 'https://opensea.io/asset/create'
    driver.get(url)
    time.sleep(0.5)
    signIntoMeta(driver, wait, isrinkeby, mnemonicString, walletPwd)
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[1])
    time.sleep(2)
    driver.find_element_by_xpath("//*[text()='Get started free']")



def signIntoMeta(driver, wait, isrinkeby, mnemonicString, walletPwd):
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[0])
    time.sleep(0.5)
    # driver.close()
    # driver.switch_to.window(tabs2[0])
    button = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button')
    button.click()
    print('meta clicked')
    time.sleep(0.5)
    button = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button')
    button.click()
    button = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[1]')
    button.click()
    time.sleep(0.5)
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
    time.sleep(1)
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
    oswalleticon = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/nav/ul/li[5]/button')
    oswalleticon.click()
    time.sleep(0.1)
    metaicon = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/aside/div[2]/div/div[2]/ul/li[1]/button')
    metaicon.click()
    time.sleep(1.5)
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[2])
    connectnext = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]')
    connectnext.click()
    time.sleep(0.5)
    connect = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]')
    connect.click()
    time.sleep(0.5)
    wait.until(ExpectedConditions.presence_of_element_located(
        (By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]')))
    sign = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]')
    sign.click()


if __name__ == '__main__':
    uploadFiles(186, 65, True,
                mnemonicString='',
                walletPwd=''
                )
