from time import sleep, time
from selenium import webdriver
from getpass4 import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import colorama
from colorama import Fore
import pyfiglet
from colored import fg
from colorama import Style

browser = webdriver.Chrome()
browser.get("https://www.instagram.com/")
sleep(2)

error = fg('red')
alert = fg('yellow')

def login(username, password):
	username_input = browser.find_element(By.CSS_SELECTOR,"input[name='username']")
	password_input = browser.find_element(By.CSS_SELECTOR,"input[name='password']")
	username_input.send_keys(Keys.CONTROL + "a")
	username_input.send_keys(Keys.DELETE)
	password_input.send_keys(Keys.CONTROL + "a")
	password_input.send_keys(Keys.DELETE)
	username_input.send_keys(username)
	password_input.send_keys(password)

	login_button = browser.find_element(By.XPATH,"//button[@type='submit']")
	login_button.click()
	sleep(5)

def accept_cookies():
	try:
		cookies = browser.find_element(By.XPATH, "//button[text()='Accept']")
		cookies.click()
	except:
		browser.find_element(By.XPATH,"//button[text()='Permitir solo cookies necesarias']").click()

def open_followers(account):
	try:
		browser.get("https://www.instagram.com/"+ account + "/followers/")
		sleep(3)
		browser.find_element(By.XPATH,"//div[text()=' seguidores']").click()
		return True
	except:
		print(error + "Error: Invalid username" + Style.RESET_ALL)
		return False

def scroll_followers(minutes):
	try:
		pop_up = browser.find_element(By.XPATH,"//div[@class='isgrP']")
		timeout = time() + 60 * minutes
		while True:
			if time() > timeout:
				break
			browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up)
			sleep(1)

		return True
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)
		return False

def follow_followers():
	try:
		list_followers = browser.find_element(By.XPATH,"//div[@class='PZuss']")
		for child in list_followers.find_element(By.CSS_SELECTOR,'li'):
			follow = child.find.find_element(By.CSS_SELECTOR,"button")
			if follow.text == "Seguir":
				follow.click()
			else:
				pass #already followed
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)

accept_cookies()

opt = True

ascii_banner = pyfiglet.figlet_format("InstaBot")
print(ascii_banner)
print("By urrea")
while opt:
	print (" ")
	print(f"1. Log In")
	print(f"2. Follow all followers of a user")
	print(f"3. Mentions in a publication")
	print(f"4. Common friends between 2 users")
	print(f"5. Exit")
	options = input("Select option [1-5]:")

	if options == '1':
		user = input("Username: ")
		passwd = getpass("Password: ")
		login(user,passwd)
	elif options == '2':
		fol = input("Select the user: ")
		if open_followers(fol):
			sleep(3)
			if scroll_followers(2):
				print(f"Following all users...")
				#follow_followers()
	elif options == '5':
		print(f"Bye...")
		browser.quit()
		opt = False
	else:
		print(f'Select a valid option')

	print(" ")
	print(alert + "Alert: Don't touch the web, the bot will not work!" + Style.RESET_ALL)