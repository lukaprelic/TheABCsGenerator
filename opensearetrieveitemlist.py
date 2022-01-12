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
    with open("nftList2.csv", 'w') as f:
        # f.write('sep=,\n')
        f.write('itemId,openSeaId,tokenId,link,sellOrders\n')
        for key, val in tokens.items():
            if str(val['sell_orders']) == 'None':
                isListed = str(val['sell_orders'])
            else:
                isListed = 'Not Listed'
            line = str(key) + ',' + str(val['id']) + ',' + str(val['token_id']) + ',' + str(val['permalink']) + ',' + isListed + '\n'
            # print(line)
            f.write(line)


if __name__ == '__main__':
    retrieveItemList(ownerHash='')
