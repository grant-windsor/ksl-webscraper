from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
#import boto3
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

# This sections is for persistence using aws s3, which allows you to store and retrieve the results of previous searches.
#s3 = boto3.resource('s3')
#s3.meta.client.download_file('cs501bucket', 'ksl_data.json', 'ksl_data.json')
#with open('ksl_data.json') as json_file:
#    priceTable = json.load(json_file)

query = input('Enter your ksl classifieds search query:\n')
q_url = ""
for word in query.split(" "):
    if word != query.split(" ")[-1]:
        q_url = q_url + word + "%20"
    else:
        q_url = q_url + word

url = "https://classifieds.ksl.com/search/keyword/" + q_url

driver.get(url)
# get a list of listings
prices = driver.find_elements(By.CLASS_NAME, "item-info-price")
result = [p.text for p in prices if p.text]

pageNum = 1
newItems = True
while newItems:
    driver.get(url + "page/" + str(pageNum))
    # print(url + "page/" + str(pageNum))
    prices = driver.find_elements(By.CLASS_NAME, "item-info-price")

    if not prices:
        newItems = False
    pageNum += 1
    
    listings = [p.text for p in prices if p.text]
    result = result + listings

vals = [float(re.sub(",", "", p[1:])) for p in result]
if vals:
    avg = sum(vals) / len(vals)
    print("prices are:")
    print(vals)
    print("the average price returned by the search: " + query + ", is $" + str(round(avg, 2)))
    #if query in priceTable:
        #print("the last time you ran this query the average price was: $" + str(round(priceTable[query], 2)))
    #priceTable[query] = avg
    #out_file = open('ksl_data.json', 'w')
    #json.dump(priceTable, out_file)
    #out_file.close()
    #s3.meta.client.upload_file('ksl_data.json', 'cs501bucket', 'ksl_data.json')

