import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
from urllib.request import Request, urlopen
import csv
import requests
import shutil
from Screenshot import Screenshot_Clipping
from selenium import webdriver 
from time import sleep 
from PIL import Image 

pd.set_option('display.max_colwidth', 25)

symbol = input('Enter a ticker: ')

ob = Screenshot_Clipping.Screenshot() 
driver = webdriver.Chrome('/Users/user/Downloads/chromedriver 2') 

url = ('http://finviz.com/quote.ashx?t=' + symbol.lower())
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
html = BS(webpage, 'html.parser')

driver.get(url) 
element = driver.find_element_by_class_name('canvas')
img_url = ob.get_element(driver, element, r'.') 

driver.close()
driver.quit()

def get_fundamentals():
    try:
        fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]

        fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        colOne = []
        colLength = len(fundamentals)
        for k in np.arange(0, colLength, 2):
            colOne.append(fundamentals[f'{k}'])
        attrs = pd.concat(colOne, ignore_index=True)
    
        colTwo = []
        colLength = len(fundamentals)
        for k in np.arange(1, colLength, 2):
            colTwo.append(fundamentals[f'{k}'])
        vals = pd.concat(colTwo, ignore_index=True)
        
        fundamentals = pd.DataFrame()
        fundamentals['coefficient'] = attrs
        fundamentals['ratio'] = vals
        fundamentals = fundamentals.set_index('coefficient')
        fundamentals.to_csv('analysis.csv')
        read_file = pd.read_csv (r'/Users/user/Documents/EDUCATION/Python/Mazars/analysis.csv')
        read_file.to_excel (r'/Users/user/Documents/EDUCATION/Python/Mazars/analysis.xlsx', index = None, header=True)
        return fundamentals

    except Exception as e:
        return e

print ('Coefficient and ratio for the company: ')
print(get_fundamentals())