from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
import re
import pandas as pd
import random
from sklearn.utils import shuffle
import requests

url_cambridge = "https://dictionary.cambridge.org/zht/詞典/英語/"
url_reverso = "https://context.reverso.net/translation/english-japanese/"
# driver = webdriver.Chrome('./chromedriver')

def queryPhrases(query):
    # driver = webdriver.Chrome('./chromedriver')
    # driver.get(url_reverso + query)
    session = requests.Session()
    r = session.get(url_reverso+query, headers={'User-Agent': 'Mozilla/5.0'})
    sel= Selector(text = r.text)
    phrases = sel.xpath('//html/body/div[@id="wrapper"]/section[@id="body-content"]/div[@class="left-content"]/section[@id="examples-content"]/div/div[@class="src ltr"]/span[@class="text"]').extract()
    # driver.close()
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
    driver.close()
    return phrases

def queryPhrases_cambridge_request(query):
    r = requests.get(url_cambridge+query)
    # print(r.text)
    sel= Selector(text = r.text)
    phrases = []
    p = re.compile(r'<.*?>')
    ph = sel.xpath('//*[@id="page-content"]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div[3]/div').extract()
    for i in ph:
        phrases.append(p.sub('',i))
    return phrases

data=pd.read_excel('zen.xlsx', index_col=None)
# words number 
data['single']=data['Q'].map(lambda x: len(x.split(" "))<=1)
single = data[data['single']]
single = shuffle(single)
single['familarity'] = single['familarity'].fillna(0)
dfout = pd.DataFrame([],columns=single.columns.values)
single = single.sort_values('familarity')
flag = True
totnum = len(single['ID'])
terminate = False

for i in range(totnum):
    count = 0 
    if terminate:
        break
    query = single.iloc[i,1]

    phrases = queryPhrases(query)
    # phrases = queryPhrases_cambridge(query)
    # phrases = queryPhrases_cambridge_request(query)
    if len(phrases) == 0:
        print("Cant find phrase for : " + query)
    while flag and count< len(phrases):
        ansIndex = random.randint(1,3)
        # quest = re.sub('\<em\>(.*?)\<\/em\>','____',phrases[count])
        quest = re.sub(query,'____',phrases[count])
        print(str(count+1) + "/" + str(len(phrases)) + ". "+ quest)
        otherIndex = []
        for j in range(1,4):
            if j == ansIndex:
                print(str(j)+". " + query)
                continue
            other = random.randint(1,totnum-2)
#            print("other: " + str(other))
            print(str(j)+". " + single.iloc[other,1])
            
        x = input()
        if x == "0":
            flag = False
        elif x== "n":
            count += 1
            continue
        elif x=="a":
            print("Ans: "+query)
            print("pronounce: " +str(single.iloc[i,2]))
            print("meaning: " +str(single.iloc[i,3]))
            print("phrase: " +str(single.iloc[i,7]))
            
            single.iloc[i,6] -= 1
            print("next?")
            y = input()
            if y == "y":
                break
            else:
                # data[data['single']] = single
                # data.to_excel("output.xlsx",index=False)
                dfout.loc[len(dfout)] = single.loc[single['Q']==query].iloc[0,:]
                dfout.to_excel("output.xlsx",index=False)
                terminate = True
                break
                
        elif x==str(ansIndex):
            # single['familarity'][i] += 1
            single.iloc[i,6] += 1
            print("correct")
            print("next?")
            y = input()
            if y == "y":
                break
            else:
                # data[data['single']] = single
                # data.to_excel("output.xlsx",index=False)
                dfout.loc[len(dfout)] = single.loc[single['Q']==query].iloc[0,:]
                dfout.to_excel("output.xlsx",index=False)
                terminate = True
                break
        else:
            # single['familarity'][i] -= 1
            single.iloc[i,6] -= 1
            print("wrong")
    dfout.loc[len(dfout)] = single.loc[single['Q']==query].iloc[0,:]

        


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