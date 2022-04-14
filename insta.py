from time import sleep, time
from selenium import webdriver
from getpass4 import getpass
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get("https://www.instagram.com/")
sleep(2)

def login(username, password):
	username_input = browser.find_element_by_css_selector("input[name='username']")
	password_input = browser.find_element_by_css_selector("input[name='password']")
	username_input.send_keys(Keys.CONTROL + "a")
	username_input.send_keys(Keys.DELETE)
	password_input.send_keys(Keys.CONTROL + "a")
	password_input.send_keys(Keys.DELETE)
	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button = browser.find_element_by_xpath("//button[@type='submit']")
	login_button.click()
	sleep(5)

def accept_cookies():
	try:
		cookies = browser.find_element_by_xpath("//button[text()='Accept']")
		cookies.click()
	except:
		browser.find_element_by_xpath("//button[text()='Permitir solo cookies necesarias']").click()

def open_followers(account):
	browser.get("https://www.instagram.com/"+ account + "/followers/")
	sleep(3)
	browser.find_element_by_xpath("//div[text()=' seguidores']").click()

def scroll_followers(minutes):
	pop_up = browser.find_element_by_xpath("//div[@class='isgrP']")
	timeout = time() + 60 * minutes
	while True:
		if time() > timeout:
			break
		browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up)
		sleep(1)

def follow_followers():
	list_followers = browser.find_element_by_xpath("//div[@class='PZuss']")
	for child in list_followers.find_element_by_css_selector('li'):
		follow = child.find.find_element_by_css_selector("button")
		if follow.text == "Seguir":
			follow.click()
		else:
			pass #already followed

accept_cookies()

opt = True

while opt:
	print(f"1. LogIn")
	print(f"2. Follow all followers of a user")
	print(f"1. Exit")
	options = input("Select option [1-3]:")
	if options == '1':
		user = input("Username: ")
		passwd = input("Password: ")
		login(user,passwd)
	elif options == '2':
		fol = input("Select the user: ")
		open_followers(fol)
		sleep(3)
		scroll_followers(2)
		#follow_followers()
	elif options == '3':
		print(f"Bye...")
		browser.quit()
		opt = False
	else:
		print(f'Select a valid option')