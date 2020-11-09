from selenium import webdriver
from bs4 import BeautifulSoup
import time
import threading, time
import mysql.connector
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

import mysql.connector

mainURL = "https://www.amazon.fr/gp/product"
ukURL = "https://www.amazon.co.uk/gp/product"
itURL = "https://www.amazon.it/gp/product"
deURL = "https://www.amazon.de/gp/product"
esURL = "https://www.amazon.es/gp/product"
secondURL = "https://www.amazon.fr/gp/offer-listing"
asinList=[]
Asin = ""
Title = ""
Root_Category = ""
Images = ""
Description = ""
Features = ""
Brand = ""
Color = ""
Price = ""
Shipping_fees = ""
Shipping_Time_Delivery = ""
isInStock = "false"
Stock_amazon_quantity = ""
Manufacturer = ""
Model = ""
Ean = ""
Rating = ""
Number_Reviews = ""
Sold_by = ""
Delivered_by = "Amazon"
Coupon = ""
isPrime = "false"
isProductNew = "false"
Seller_name = ""
Seller_rating = ""
Seller_number_reviews = ""
IT_Price = ""
IT_isInStock = ""
IT_Shipping_fees = ""
UK_Price = ""
UK_isInStock = ""
UK_Shipping_fees = ""
DE_Price = ""
DE_isInStock = ""
DE_Shipping_fees = ""
ES_Price = ""
ES_isInStock = ""
ES_Shipping_fees = ""

with open("asinlistJson.rtf") as infile:
    for line in infile:
    	if line.find("asin") != -1:
    		asinList.append(line.split(":")[1].strip()[1:11])

print("ASIN : 1 ~ " + str(len(asinList)))

nStart = int(input("Please input the Start number: "))
nEnd = int(input("Please input the End number: "))

PROXY = "mixed.rotating.proxyrack.net:444"
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument("--headless") 
options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )

# mydb = mysql.connector.connect(
#   host="127.0.0.1",
#   user="beezup",
#   password="amazon123",
#   database="amazon"
# )
# mycursor = mydb.cursor()

for i in range(nStart - 1, nEnd):
	Asin = asinList[i]
	url = f'{mainURL}/{asinList[i]}'
	driver.get(url)
	time.sleep(1)

	soup = BeautifulSoup(driver.page_source, "html.parser")

	try:
		TitleItem = soup.find(id='productTitle')
		if TitleItem:
			Title = TitleItem.text.strip()
	except:
		pass

	try:
		Root_Category = driver.find_element_by_xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[1]/span/a').text.strip()
	except:
		pass

	try:
		ImageItem = soup.find("img", id='landingImage')
		if ImageItem:
			Images = ImageItem['src']
	except:
		pass

	try:
		DescriptionItem = soup.find(id='productDescription')
		if DescriptionItem:
			Description = DescriptionItem.text.strip()
	except:
		pass

	try:
		FeaturesItem = soup.find(id='feature-bullets')
		if FeaturesItem:
			Features = FeaturesItem.text.strip()
	except:
		pass

	try:
		TableItem_Loof = soup.find_all("th", class_="prodDetSectionEntry")
		if TableItem_Loof:
			for j in range(1, len(TableItem_Loof) + 1):
				temp = driver.find_element_by_xpath('//table[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(j)+']/th').text.strip()
				if temp == "Marque":
					Brand = driver.find_element_by_xpath('//table[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(j)+']/td').text.strip()

				if temp == "Couleur":
					Color = driver.find_element_by_xpath('//table[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(j)+']/td').text.strip()

				if temp == "Fabricant":
					Manufacturer = driver.find_element_by_xpath('//table[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(j)+']/td').text.strip()

				if temp == "Numéro du modèle":
					Model = driver.find_element_by_xpath('//table[@id="productDetails_techSpec_section_1"]/tbody/tr['+str(j)+']/td').text.strip()
	except:
		pass

	try:
		TableEANItem_Loof = soup.find_all("th", class_="a-span4")
		if TableEANItem_Loof:
			for j in range(1, len(TableEANItem_Loof) + 1):
				temp = driver.find_element_by_xpath('//table[@id="product-specification-table"]/tbody/tr['+str(j)+']/th').text.strip()
				if temp == "Ean":
					Ean = driver.find_element_by_xpath('//table[@id="product-specification-table"]/tbody/tr['+str(j)+']/td').text.strip()
	except:
		pass

	try:
		PriceItem = soup.find(id='price_inside_buybox')
		if PriceItem:
			Price = PriceItem.text.strip().replace(",", ".")
	except:
		pass

	try:
		Shipping_fees = driver.find_element_by_xpath('//span[@id="price-shipping-message"]/b').text.strip()
		Shipping_fees_Temp = Shipping_fees.split(" ")
		Shipping_fees = "0.0 €"
		for temp in Shipping_fees_Temp:
			if temp.find(",") != -1:
				Shipping_fees = temp.replace(",", ".")
				if Shipping_fees.find("€") == -1:
					Shipping_fees += " €"
	except:
		Shipping_fees = "0.0 €"

	try:
		Shipping_Time_Delivery = driver.find_element_by_xpath('//div[@id="ddmDeliveryMessage"]/b').text.strip()
		Shipping_Time_Temp = Shipping_Time_Delivery.split(" ")
		if len(Shipping_Time_Temp) == 5:
			Shipping_Time_Delivery = str(int(Shipping_Time_Temp[3]) + 30 - int(Shipping_Time_Temp[0]))
		elif len(Shipping_Time_Temp) == 4:
			Shipping_Time_Delivery = str(int(Shipping_Time_Temp[2]) - int(Shipping_Time_Temp[0]))
	except:
		Shipping_Time_Delivery = ""

	if Shipping_Time_Delivery == "sélectionnez cette option lors de votre commande":
		Shipping_Time_Delivery = ""

	try:
		isInStock = driver.find_element_by_xpath('//div[@id="availability"]/span').text.strip()
		if isInStock == "En stock.":
			isInStock = "true"
			Stock_amazon_quantity = "0"
		else:
			Stock_amazon_quantity = isInStock.split(" ")[5]
			isInStock = "true"
	except:
		isInStock = "false"
		Stock_amazon_quantity = "0"

	if Stock_amazon_quantity == "vendeurs.":
		Stock_amazon_quantity = "0"
	elif Stock_amazon_quantity == "2020.":
		Stock_amazon_quantity = "0"

	try:
		Rating = soup.find(id='acrPopover').get("title").strip().split(" ")[0].replace(",", ".")
	except:
		pass

	try:
		Number_Reviews = soup.find(id='acrCustomerReviewText').text.strip().split(" ")[0]
	except:
		pass

	try:
		Sold_by = driver.find_element_by_xpath('//div[@id="merchant-info"]/a[1]').text.strip()
	except:
		pass

	if Sold_by == "":
		Sold_by = "Amazon"

	try:
		Coupon = driver.find_element_by_xpath('//div[@id="vpcButton"]/div/label/span/span').text.strip()
	except:
		pass

	try:
		PrimeTemp = soup.find_all("i", class_="a-icon-prime")
		if PrimeTemp:
			isPrime = "true"
	except:
		pass

	try:
		NewTemp = soup.find(id='olp-upd-new')
		if NewTemp:
			isProductNew = "true"
	except:
		pass

	url = f'{itURL}/{asinList[i]}'
	driver.get(url)

	try:
		IT_Price = driver.find_element_by_xpath('//span[@id="price_inside_buybox"]').text.strip().replace(",", ".")
	except:
		pass

	try:
		IT_isInStock = driver.find_element_by_xpath('//div[@id="availability"]/span').text.strip()
		if IT_isInStock == "En stock.":
			IT_isInStock = "true"
		else:
			IT_isInStock = "true"
	except:
		IT_isInStock = "false"

	try:
		IT_Shipping_fees = driver.find_element_by_xpath('//span[@id="price-shipping-message"]/b').text.strip()
		IT_Shipping_fees_Temp = IT_Shipping_fees.split(" ")
		IT_Shipping_fees = "0.0 €"
		for temp in IT_Shipping_fees_Temp:
			if temp.find(",") != -1:
				IT_Shipping_fees = temp.replace(",", ".")
				if IT_Shipping_fees.find("€") == -1:
					IT_Shipping_fees += " €"
	except:
		IT_Shipping_fees = "0.0 €"

	url = f'{ukURL}/{asinList[i]}'
	driver.get(url)

	try:
		UK_Price = driver.find_element_by_xpath('//span[@id="price_inside_buybox"]').text.strip().replace(",", ".")
	except:
		pass

	try:
		UK_isInStock = driver.find_element_by_xpath('//div[@id="availability"]/span').text.strip()
		if UK_isInStock == "En stock.":
			UK_isInStock = "true"
		else:
			UK_isInStock = "true"
	except:
		UK_isInStock = "false"

	try:
		UK_Shipping_fees = driver.find_element_by_xpath('//span[@id="price-shipping-message"]/b').text.strip()
		UK_Shipping_fees_Temp = UK_Shipping_fees.split(" ")
		UK_Shipping_fees = "0.0 €"
		for temp in UK_Shipping_fees_Temp:
			if temp.find(",") != -1:
				UK_Shipping_fees = temp.replace(",", ".")
				if UK_Shipping_fees.find("€") == -1:
					UK_Shipping_fees += " €"
	except:
		UK_Shipping_fees = "0.0 €"

	url = f'{deURL}/{asinList[i]}'
	driver.get(url)

	try:
		DE_Price = driver.find_element_by_xpath('//span[@id="price_inside_buybox"]').text.strip().replace(",", ".")
	except:
		pass

	try:
		DE_isInStock = driver.find_element_by_xpath('//div[@id="availability"]/span').text.strip()
		if DE_isInStock == "En stock.":
			DE_isInStock = "true"
		else:
			DE_isInStock = "true"
	except:
		DE_isInStock = "false"

	try:
		DE_Shipping_fees = driver.find_element_by_xpath('//span[@id="price-shipping-message"]/b').text.strip()
		DE_Shipping_fees_Temp = DE_Shipping_fees.split(" ")
		DE_Shipping_fees = "0.0 €"
		for temp in DE_Shipping_fees_Temp:
			if temp.find(",") != -1:
				DE_Shipping_fees = temp.replace(",", ".")
				if DE_Shipping_fees.find("€") == -1:
					DE_Shipping_fees += " €"
	except:
		DE_Shipping_fees = "0.0 €"

	url = f'{esURL}/{asinList[i]}'
	driver.get(url)

	try:
		ES_Price = driver.find_element_by_xpath('//span[@id="price_inside_buybox"]').text.strip().replace(",", ".")
	except:
		pass

	try:
		ES_isInStock = driver.find_element_by_xpath('//div[@id="availability"]/span').text.strip()
		if ES_isInStock == "En stock.":
			ES_isInStock = "true"
		else:
			ES_isInStock = "true"
	except:
		ES_isInStock = "false"

	try:
		ES_Shipping_fees = driver.find_element_by_xpath('//span[@id="price-shipping-message"]/b').text.strip()
		ES_Shipping_fees_Temp = ES_Shipping_fees.split(" ")
		ES_Shipping_fees = "0.0 €"
		for temp in ES_Shipping_fees_Temp:
			if temp.find(",") != -1:
				ES_Shipping_fees = temp.replace(",", ".")
				if ES_Shipping_fees.find("€") == -1:
					ES_Shipping_fees += " €"
	except:
		ES_Shipping_fees = "0.0 €"

	if isProductNew == "true":
		url = f'{secondURL}/{asinList[i]}'
		driver.get(url)
		time.sleep(1)

		try:
			Seller_name = driver.find_element_by_xpath('//div[@id="olpOfferList"]/div/div/div[2]/div[3]/h3/span/a').text.strip()
			Seller_rating = driver.find_element_by_xpath('//div[@id="olpOfferList"]/div/div/div[2]/div[3]/p/a/b').text.strip().split(" ")[0]
			Seller_number_reviews = driver.find_element_by_xpath('//div[@id="olpOfferList"]/div/div/div[2]/div[3]/p').text.strip()
			Seller_number_reviews = Seller_number_reviews.split(" ")[8] + Seller_number_reviews.split(" ")[9]
			Seller_number_reviews = Seller_number_reviews[1:]
		except:
			pass

		if Seller_number_reviews.find("évaluations") != -1:
				Seller_number_reviews = Seller_number_reviews.replace("évaluations", "")

	# sql = "DELETE FROM products WHERE Asin = '" + Asin + "'"
	# mycursor.execute(sql)
	# mydb.commit()

	# sql = "INSERT INTO products (Asin, Ean, Title, Description, Features, Images, Root_Category, Brand, Model, Price, Shipping_fees, Shipping_Time_Delivery, Sold_by, Delivered_by, Seller_name, Seller_rating, Seller_number_reviews, isPrime, isInStock, Stock_amazon_quantity, isProductNew, Rating, Number_Reviews, Coupon, UK_Price, UK_Shipping_fees, UK_isInStock, IT_Price, IT_Shipping_fees, IT_isInStock, DE_Price, DE_Shipping_fees, DE_isInStock, ES_Price, ES_Shipping_fees, ES_isInStock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	# val = (Asin, Ean, Title, Description, Features, Images, Root_Category, Brand, Model, Price, Shipping_fees, Shipping_Time_Delivery, Sold_by, Delivered_by, Seller_name, Seller_rating, Seller_number_reviews, isPrime, isInStock, Stock_amazon_quantity, isProductNew, Rating, Number_Reviews, Coupon, UK_Price, UK_Shipping_fees, UK_isInStock, IT_Price, IT_Shipping_fees, IT_isInStock, DE_Price, DE_Shipping_fees, DE_isInStock, ES_Price, ES_Shipping_fees, ES_isInStock)
	# mycursor.execute(sql, val)
	# mydb.commit()
	print(Root_Category)


		

			
