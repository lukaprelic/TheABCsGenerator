import os

import pandas
from selenium import webdriver
import time


def uploadFiles(startItemId):
    chop = webdriver.ChromeOptions()
    chop.add_extension('MetaMask_v10.0.2.crx')
    driver = webdriver.Opera(options=chop)
    df = pandas.read_csv('Generated/metadata.csv')
    driver.get('https://testnets.opensea.io/asset/create')
    time.sleep(0.5)
    signIntoMeta(driver)
    tabs2 = driver.window_handles
    driver.switch_to.window(tabs2[1])
    time.sleep(2)
    #print('Starting with item id:', startItemId - 51)
    for index, row in df.iterrows():
        print('first row:', index, row)
        if index > 0:
            createPage = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div[1]/nav/ul/li[4]/a')
            createPage.click()
        print("ROW:", row)
        print(row['Id'], row['Background'], row['Font'], row['Font & Colour Combination'],
              row['Font Colour'], row['Hat'], row['Letter1'], row['Letter2'],
              row['Letter3'], row['Letter Permutation'], row['Special'])
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath('Generated\\51 ABCs SLN None.png')
        imageUpload.send_keys(imagePath)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys('The ABCs #{}'.format(row['Id']))
        description = driver.find_element_by_xpath('//*[@id="description"]')
        description.send_keys(row['Letter Permutation'])
        collectionName = driver.find_element_by_xpath(
            '//*[@id="__next"]/div[1]/main/div/div/section/div/form/section[5]/div/input')
        collectionName.send_keys('TheABCs')
        collectionPlusButton = driver.find_element_by_xpath(
            '//*[@id="__next"]/div[1]/main/div/div/section/div/form/section[6]/div[1]/div/div[2]/button')
        collectionPlusButton.click()
        time.sleep(1.5)
        print('starting properties population')
        for i, (key, value) in enumerate(row.items()):
            if key in ['Id', 'Special']:
                continue
            collectionAddPropButton = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/section/button')
            collectionAddPropButton.click()
            print('index: ', i, i + 1)
            propInputKeyXpath = (
                '/html/body/div[2]/div/div/div/section/table/tbody/tr[{}]/td[1]/div/div/input'.format(i + 1))
            print('propInputKeyXpath', propInputKeyXpath)
            propKey = driver.find_element_by_xpath(
                propInputKeyXpath)
            propKey.send_keys(key)
            propKey = driver.find_element_by_xpath(
                ('/html/body/div[2]/div/div/div/section/table/tbody/tr[{}]/td[2]/div/div/input'.format(i + 1)))
            propKey.send_keys(value)
        propSave = driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/footer/button')
        propSave.click()
        print('completed properties population')
        time.sleep(0.5)
        createNFT = driver.find_element_by_xpath(
            '//*[@id="__next"]/div[1]/main/div/div/section/div/form/div/div[1]/span/button')
        createNFT.click()
        print('creating nft ', row['Id'], row['Background'], row['Font'], row['Font & Colour Combination'],
              row['Hat'], row['Letter Permutation'])
        time.sleep(5)
        closeCreateModal = driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[2]/button/i')
        closeCreateModal.click()

        time.sleep(500)


def signIntoMeta(driver):
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
    print(button)
    button.click()
    print('import clicked')
    button = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[1]')
    print('no thanks clicked')
    button.click()
    time.sleep(0.5)
    mnemonicInput = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[1]/div/input')
    mnemonicInput.send_keys('april chef unlock damage exclude man direct green slice grape uncover upper')
    pwd1Input = driver.find_element_by_xpath(
        '//*[@id="password"]')
    pwd1Input.send_keys('Luka.1993')
    pwd2Input = driver.find_element_by_xpath(
        '//*[@id="confirm-password"]')
    pwd2Input.send_keys('Luka.1993')
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
    print(tabs2)
    driver.switch_to.window(tabs2[2])
    connectnext = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]')
    connectnext.click()
    time.sleep(0.5)
    connect = driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]')
    connect.click()
    time.sleep(1.5)
    sign = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]')
    sign.click()


if __name__ == '__main__':
    uploadFiles(101)
