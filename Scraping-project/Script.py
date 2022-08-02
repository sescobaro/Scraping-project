from selenium import webdriver
from bs4 import BeautifulSoup
try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)
import pandas as pd


#Using MS Edge as browser, I downladed the webdriver from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
driver = webdriver.Edge(executable_path=r'msedgedriver.exe')
driver.get('https://www.facebook.com/Megatiendavirtual/posts/4631284193560254')

products=[]

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

#💪🏼 is the first chracter in every line that has a product
for line in soup.find_all('p'):   
    tline=line.text
    tline=tline.rstrip()
    sline=re.split('💪🏼', tline)
    products.append(sline)
  

brands_lst=(products[1::2])
brands_str=[]


for brand in brands_lst:
    brand=brand[0].replace('.','')
    brand=brand.strip()
    brands_str.append(brand)
    

cel_lst=(products[0::2])
cel_str1=[]


for cel in cel_lst:
    cel_str1.append(cel)

cel_str=cel_str1[1:]

#Using for and globals to create each variable
for i in range(0, len(brands_str)):
    globals()[f"brand{i}"] = cel_str[i]


i=0
for i in range(0, len(brands_str)):
    globals()[f"pri{i}"] = []
    globals()[f"pro{i}"] = []

#create dataframe
def f(brand, pri, pro):
    for word in brand:   
        priPos=word.find('$')
        price=word[priPos:]
        product=word[:priPos]
        pri.append(price)
        pro.append(product)

i=0
while 0<=i<len(brands_str):
    f(globals()[f"brand{i}"], globals()[f"pri{i}"], globals()[f"pro{i}"])
    i=i+1

Tienda='Megatienda'

i=0
for i in range(0, len(brands_str)):
    globals()[f"brand{i}"]=globals()[f"brand{i}"][1:]

#Data frames are created for each brand
i=0
while 0<=i<len(brands_str):
    globals()[f"dfbrand{i}"] = pd.DataFrame({'Phone':globals()[f"pro{i}"],'Price':globals()[f"pri{i}"], 'Brand':brands_str[i], 'Store':Tienda})
    i=i+1

#The first row is empty
i=0
for i in range(0, len(brands_str)):
    globals()[f"dfbrand{i}"]=globals()[f"dfbrand{i}"][1:]


#A xlsx file is created
i=0
with pd.ExcelWriter(r'List.xlsx') as writer:   
    while 0<=i<len(brands_str):
        globals()[f"dfbrand{i}"].to_excel(writer, sheet_name=brands_str[i])
        i=i+1

#Connection is closed
driver.quit()