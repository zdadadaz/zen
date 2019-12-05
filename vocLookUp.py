from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
import re
import pandas as pd
import random

url_cambridge = "https://dictionary.cambridge.org/zht/詞典/英語/"
url_reverso = "https://context.reverso.net/translation/english-japanese/"
# driver = webdriver.Chrome('./chromedriver')

def queryPhrases(query):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url_reverso + query)
    sel= Selector(text = driver.page_source)
    phrases = sel.xpath('//html/body/div[@id="wrapper"]/section[@id="body-content"]/div[@class="left-content"]/section[@id="examples-content"]/div/div[@class="src ltr"]/span[@class="text"]').extract()
    driver.close()
    return phrases

def queryPhrases_cambridge(query):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url_cambridge + query)
    sel= Selector(text = driver.page_source)
    phrases = []
    p = re.compile(r'<.*?>')
    ph = sel.xpath('//*[@id="page-content"]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div[3]/div').extract()
    for i in ph:
        phrases.append(p.sub('',i))
    meaning = sel.xpath('//*[@id="page-content"]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div').extract()
    meaning = (p.sub('',meaning[0]))
    kk = sel.xpath('//*[@id="page-content"]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[2]/span[2]/span[3]/span').extract()
    if len(kk) == 0:
        kk = ''
    else:
        kk = p.sub('',kk[0])
    dict_info = {}
    dict_info['phrases'] = phrases
    dict_info['means'] = meaning
    dict_info['kk'] = kk
    driver.close()
    return dict_info


data=pd.read_excel('output.xlsx', index_col=None)
# words number 
data['familarity'] = data['familarity'].fillna(0)
flag = True
totnum = len(data['ID'])
terminate = False
for i in range(8,totnum):
    count = 0 
    if terminate:
        break
    query = data.iloc[i,1]

    # phrases = queryPhrases(query)
    dict_info = queryPhrases_cambridge(query)
    phrases = dict_info['phrases']
    if len(phrases) == 0:
        print("Cant find phrase for : " + query)
        continue
    data.iloc[i,2] = dict_info['kk']
    data.iloc[i,4] = dict_info['means']
    for p in range(len(dict_info['phrases'])):
        if p < 3:
            data.iloc[i,7+p] = phrases[p]
        else:
            break
    data.to_excel("output_test.xlsx",index=False)


    



        


# class vocSpider(Spider):
#     name = 'vocabularies'
#     allowed_domains = ['https://context.reverso.net/translation/english-japanese/']
#     def start_requests(self):
#         self.driver = webdriver.Chrome('./chromedriver')
#         self.driver.get('https://context.reverso.net/translation/english-japanese/familiarity')
#         sel = Selector(text=self.driver.page_source)
#         phrases = sel.xpath('//html/body/div[@id="wrapper"]/section[@id="body-content"]/div[@class="left-content"]/section[@id="examples-content"]/div/div[@class="src ltr"]/span[@class="text"]').extract()
#         print(phrases)
#         self.driver.close()
#         pass