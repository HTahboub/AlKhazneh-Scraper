from selenium import webdriver
import requests
import time as t
import os as os
from clint.textui import progress
import platform as p
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS('bin/phantomjs')

root = "/user/profile.php?id="
baseurl = "http://alkhazneh.kingsacademy.edu.jo/"
username = "hamzatahboub21@kingsacademy.edu.jo"
password = "REDACTED"

def login(username, password):
	c = requests.Session()

	driver.get("http://alkhazneh.kingsacademy.edu.jo/login/index.php")
	driver.find_element_by_id('username').send_keys(username)
	driver.find_element_by_id('password').send_keys(password)
	driver.find_element_by_id('loginbtn').click()
	SESS = driver.find_element_by_name('sesskey').get_attribute('value')
	print('Successfully logged in!')

	cookies = driver.get_cookies()
	for cookie in cookies:
		c.cookies.set(cookie['name'], cookie['value'])

	return c

def return_name(ID, c):
	r = c.get(baseurl + root + str(ID))

	if (r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')
		return soup.find('h1').text

	else:
		print('ERROR: ' + str(r.status) + ' ' + r.reason)
		sys.exit()

# limit is the brute-force max
def write_names_ids(limit):
	c = login(username, password)
	f = open("names_IDs.txt", "w")
	percent = 10

	for i in range(limit):
		name = return_name(i, c)
		if i > percent*limit/100:
			print("Percent Complete: {}".format(percent))
			percent += 10
		if name != '': f.write("ID: {}, Name: {},\n".format(i, name))

	print("All names and IDs successfully printed!")
	f.close()

def find_courses(ID):
	c = login(username, password)
	r = c.get(baseurl + root + str(ID))

	if (r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')
		list = soup.findAll('ul')[5].findAll('li')
		out = []
		for element in list: out.append(element.text)
		return out

	else:
		print('ERROR: ' + str(r.status) + ' ' + r.reason)
		sys.exit()

# print(find_courses(1863))
write_names_ids(150000)
