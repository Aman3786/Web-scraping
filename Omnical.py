# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import requests
import os


# %%
edge_path = "res\\msedgedriver.exe"
driver       = webdriver.Edge(executable_path = edge_path)


# %%
REQUIREMENTS = "res\\company_names.txt"
OUTPUT_FILE  = "Outputs\\output.csv"
DATA_FIELDS  = ['Sr.no',
                'Brand',
                'Manufacture Part No.',
                'Product Image Link',
                'Description',
                'Price Symbol',
                'Price',
                'Category',
                'Sub-Category1',
                'Sub-Category2']
BASE        = "https://www.omnical.com/manufacturer/"
with open(REQUIREMENTS) as f:
    output = f.read()

# Getting all the data into list
brand_list = output.split("\n")



url = BASE+str(brand_list[4])
print(url)
driver.get(url

file = r'C:\Users\Arbaaz\Desktop\last\E\Eleq\Eleq.csv'

if not os.path.exists(file):
    csv_file = open(file,'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Sr.no','Brand','Manufacture Part No.','Product Image Link','Description','Price Symbol','Price','Category','Sub-Category1','Sub-Category2'])
else:
    csv_file = open(file,'a')
    csv_writer = csv.writer(csv_file)


alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','X','Z']

chrome_path = r"C:\Users\Arbaaz\Desktop\\chromedriver.exe"
driver      = webdriver.Chrome(executable_path=chrome_path)

# name change
driver.get('https://www.omnical.co/manufacturer/Eleq?page=1&q=&autoclass=false&searchType=brand&f_series=&f_classcode=&f_brand=Eleq&getImages=false')

# Will be used to hold product element rows
product_list = {}

# Start and ending number of the product rows in the page
START_ELEMENT_NUMBER = 0
END_ELEMENT_NUMBER   = 9

# Getting the last page of the total results
last_page = driver.find_element_by_xpath('//a[@rel="last"]').get_attribute('page')
print("The last page is {}".format(last_page))

# Looping through the entire products results, from 2nd page to the last page
# Second page because we will already be on the first page so, increment won't work
# We increment the page by clicking on the next page after the inner loop is over
p = 0
for k in alpha[p:p+1]:
    product_list[k] = []
    for i in range(2, int(last_page)+1):
        
        # There are 10 results on each page, named as products-row-(number)
        # So we loop throught all the product rows and store their element, which include
        # text, image etc details and store those elements text value in the product_list object we declared earlier
        # We can refine the elements further to get the needed values
        
        for j in range(START_ELEMENT_NUMBER, END_ELEMENT_NUMBER + 1):

            element = driver.find_element_by_id("product-row-"+str(j))
            element_code = element.get_attribute("innerHTML")

            link = element.find_element_by_class_name("tradeproduct-details-button").get_attribute("href")
            print(link)
            product_list[k].append(link)
        print()

        # Clicking on the next result page
        driver.find_element_by_xpath('//a[@page="{}"]'.format(i)).click()
        time.sleep(4.5)
    

print(product_list)

for i,j in product_list.items():
    for links in j:
        res = requests.get(links).text
        soup = BeautifulSoup(res,'lxml')
       
        
        try:
            try:
                brand = soup.find_all('div',class_='brand')
            except:
                print('No Brands')
                
            try:
                desc = soup.find_all('div',class_='product-title')
            except:
                print('No desc')
                
            try:
                mfd = soup.find_all('span',{'itemprop':'productID'})
            except:
                print('No mfd')
                
            try:
                img = soup.find('div',class_='product-detail-image').find('img').get('src')
                if img.startswith('/SiteContent'):
                    img = 'No Image Link'
            except:
                print('No Image Link')
                
            try:
                des1 = soup.find_all('div',class_='product-group')
            except:
                des1 = ''
                
            try:
                price  = soup.find_all('span',{'itemprop':'price'})
            except:
                print('no price')
                
            try:
                pricesymbol = soup.find_all('span',{'itemprop':'pricecurrency'})
            except:
                print('no symbol')
  
            categ = []
            for cat in soup.find_all('span',{'itemprop':'itemListElement'}):
                categ.append(cat.find('span',{'itemprop':'name'}))
            
            catt = categ[0]
                
            try:
                subcatt1 = categ[1].text
            except:
                subcatt1 = 'No subCategory1'
                
            try:
                subcatt2 = categ[2].text
            except:
                subcatt2 = 'No subCategory2'

        
            for m in range(len(brand)):
                brandd = brand[m].text
                despo = desc[m].text + des1[m].text
                mfdt = mfd[m].text
                imgg = img
                catte = catt.text
                subcatte1 = subcatt1
                subcatte2 = subcatt2
                pricee = price[m].text

                pricesymbole = pricesymbol[m].text
                print()

                try:
                    print('start')
                    csv_writer.writerow([m+1,brandd,mfdt,imgg,despo,pricesymbole,pricee,catte,subcatte1,subcatte2])
                    if imgg == 'No Image Link':
                        pass
                    else:
                        img_data = requests.get(imgg).content
                        with open(r'C:\Users\Arbaaz\Desktop\last\E\Eleq\Eleq images\{}_{}_{}_{}.jpg'.format(brandd,mfdt,subcatt1,subcatt2),'wb') as handler:
                            handler.write(img_data)
                        
                    print('done')
                    time.sleep(1)
                    
                except Exception as e:
                    print(e)
                    
        except:
            print("Error")

    csv_file.close()







try:
    try:
        brand = soup.find_all('div',class_='brand')
    except:
        print('No Brands')
        
    try:
        desc = soup.find_all('div',class_='product-title')
    except:
        print('No desc')
        
    try:
        mfd = soup.find_all('span',{'itemprop':'productID'})
    except:
        print('No mfd')
        
    try:
        img = soup.find('div',class_='product-detail-image').find('img').get('src')
        if img.startswith('/SiteContent'):
            img = 'No Image Link'
    except:
        print('No Image Link')
        
    try:
        des1 = soup.find_all('div',class_='product-group')
    except:
        des1 = ''
        
    try:
        price  = soup.find_all('span',{'itemprop':'price'})
    except:
        print('no price')
        
    try:
        pricesymbol = soup.find_all('span',{'itemprop':'pricecurrency'})
    except:
        print('no symbol')
    categ = []
    for cat in soup.find_all('span',{'itemprop':'itemListElement'}):
        categ.append(cat.find('span',{'itemprop':'name'}))
    
    catt = categ[0]
        
    try:
        subcatt1 = categ[1].text
    except:
        subcatt1 = 'No subCategory1'
        
    try:
        subcatt2 = categ[2].text
    except:
        subcatt2 = 'No subCategory2'