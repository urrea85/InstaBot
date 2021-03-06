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
from os import remove
from os.path import exists
import pdb
import random


browser = webdriver.Chrome()
browser.get("https://www.instagram.com/")
sleep(2)

error = fg('red')
alert = fg('yellow')

profile = ""

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

def scroll_followers(fol):
	try:
		before = ""
		if fol: #if true scrolling the followers, else the following
			seguidores = int(browser.find_element(By.XPATH,"//div[text()=' seguidores']/span").text.replace(".",""))
		else:
			seguidores = int(browser.find_element(By.XPATH,"//div[text()=' seguidos']/span").text.replace(".",""))
		
		segundos = seguidores / 4 #ratio of scroll

		if segundos < 10.0:
			segundos = 10.0
		
		if segundos > 60:
			print(f"The scroll has a duration of {segundos/60} minutes")
		else:
			print(f"The scroll has a duration of {segundos} seconds")
		pop_up = browser.find_element(By.XPATH,"//div[@class='isgrP']")
		timeout = time() + segundos
		while True:
			if time() > timeout:
				break
			browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up)
			#Divs=pop_up.find_element(By.CSS_SELECTOR,'li:last-child')
			"""if(Divs.text == before):
				print(f"El causante {before}")
				break
			else:
				before = Divs.text"""
			sleep(1)

		return True
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)
		return False

def follow_followers():
	try:
		list_followers = browser.find_element(By.XPATH,"//div[@class='PZuss']")
		for child in list_followers.find_elements(By.CSS_SELECTOR,'li'):
			follow = child.find_element(By.CSS_SELECTOR,"button")
			if follow.text == "Seguir":
				follow.click()
				sleep(random.randint(1,2))
				name = child.find_element(By.CSS_SELECTOR, "span")
				if child.find_element(By.CSS_SELECTOR,"button").text == "Seguir":
					print("Instagram does not allow to follow more accounts, try it again in a few minutes")
				else:
					print(name.text)
					file = open("followed.txt","a")
					file.write(name.text+'\n')
					file.close()
			else:
				pass #already followed
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)

def unfollow(username,filename):
	try:
		browser.get(f"https://www.instagram.com/{username}/following/")

		sleep(1)
		try:
			nuevo = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[2]/div/div[2]/div/span/span[1]/button")
		except:
			try:
				nuevo = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
			except:
				try:
					nuevo = browser.find_element(By.XPATH,"//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/button")
				except:
					nuevo = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button")
		nuevo.click()
		sleep(1)
		new = browser.find_element(By.XPATH, "//button[text()='Dejar de seguir']")
		new.click()
		sleep(2)
	except:
		print(username)
		if(username != "" ):
			file = open(filename,"a")
			file.write(username+'\n')
			file.close()
		print(error + "Error: Try it again" + Style.RESET_ALL)



def unfollow_all(filename):
	try:
		file = open(filename,"r") #r para leer, si no existe el fichero da error
		contenido = file.readlines()
		file.close()
		remove(filename)
		for line in contenido:
			user = line.strip("\n")
			print(f"Unfollowing {user}")
			unfollow(user, filename)
		print("All users unfollowed succesfully")
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)

def backup_of_followers():
	try:
		browser.get(f"https://www.instagram.com/{profile}/")
		sleep(1)
		browser.find_element(By.XPATH,"//div[text()=' seguidos']").click()
		sleep(1)
		print(f"Loading...")
		scroll_followers(False)
		print("Reading users..")
		list_followers = browser.find_element(By.XPATH,"//div[@class='PZuss']")
		for child in list_followers.find_elements(By.CSS_SELECTOR,'li'):
			follow = child.find_element(By.CSS_SELECTOR,"button")
			if follow.text == "Siguiendo":
				name = child.find_element(By.CSS_SELECTOR, "span")
				print(name.text)
				file = open("backup.txt","a")
				file.write(name.text+'\n')
				file.close()
		print(f"Backup: OK")
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)


def follow_all(filename):
	try:
		file = open(filename,"r")
		lines = file.readlines()
		file.close()

		for line in lines:
			user = line.strip("\n")
			print(f"Following {user}")
			follow(user)
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)



def follow(username):
	try:
		browser.get(f"https://www.instagram.com/{username}/")
		try:
			fol = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button")
		except:
			try:
				fol = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button")
			except:
				try:
					fol = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
				except:
					fol = browser.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div/button")
		fol.click()
		sleep(2)
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)

def followers_of_user(username):
	try:
		print("Reading users..")
		list_followers = browser.find_element(By.XPATH,"//div[@class='PZuss']")
		for child in list_followers.find_elements(By.CSS_SELECTOR,'li'):
			name = child.text.split()[0]
			fileName = username + ".txt"
			file = open(fileName,"a")
			file.write(name+'\n')
			file.close()
		print(f"Followers of {username} done.")
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)

def followings_of_user(username):
	try:
		browser.get(f"https://www.instagram.com/{username}/")
		sleep(1)
		browser.find_element(By.XPATH,"//div[text()=' seguidos']").click()
		sleep(1)
		scroll_followers(False)
		print("Reading users..")
		list_followers = browser.find_element(By.XPATH,"//div[@class='PZuss']")
		for child in list_followers.find_elements(By.CSS_SELECTOR,'li'):
			name = child.text.split()[0]
			fileName = username + ".txt"
			file = open(fileName,"a")
			file.write(name+'\n')
			file.close()
		print(f"Followers of {username} done.")
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)


def matches(user1, user2):
	try:
		print("User matches: ")
		file1 = open(user1 + ".txt", 'r')
		follows1 = file1.readlines()
		file1.close()
		cont = 0

		for fol1 in follows1:
			if fol1 != '\n':
				file2 = open(user2 + ".txt",'r')
				follows2 = file2.readlines()
				for fol2 in follows2:
					if fol1.split("\n") == fol2.split("\n"):
						cont = cont + 1
						print(fol1)
						file = open("matches.txt","a")
						file.write(fol1+'\n')
						file.close()
		print(f"{cont} matches between {user1} and {user2}")
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)


def mentions(filename,num):

	try:
		file = open(filename, 'r')
		users = file.read().split("\n")
		file.close()
		i = 0
		while i < len(users):
			commentary = ""
			for j in range(0,num):
				if j >= len(users):
					break
				commentary = commentary +  " @" + users[i+j]
			
			i = i + num
			comments = browser.find_element(By.CSS_SELECTOR,"textarea")
			comments.send_keys(commentary)
			button = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/button")
			button.click()
			sleep(60)
	except:
		print(error + "Error: Try it again" + Style.RESET_ALL)

accept_cookies()

opt = True

ascii_banner = pyfiglet.figlet_format("InstaBot")
print(ascii_banner)
print("By urrea")

#MAYBE I CAN STOP IT THE FOLLOWING BY ENTERING CTRL+C

while opt:
	print (" ")
	print(f"1. Log In") #OK
	print(f"2. Follow all followers of a user") #OK
	print(f"3. Unfollow all users followed by the bot") #OK
	print(f"4. Mention N users in a publication (For raffers)") #OK
	print(f"5. Common friends between 2 users") #OK
	print(f"6. Backup of following users") #OK
	print(f"7. Execute your backup (Follows all of your backup users)")
	print(f"8. Unfollow all (0 following)") #OK
	print(f"9. Exit") #OK
	options = input("Select option [1-9]:")

	if options == '1':
		user = input("Username: ")
		passwd = getpass("Password: ")
		profile = user
		login(user,passwd)
	elif options == '2':
		fol = input("Select the user: ")
		if open_followers(fol):
			sleep(3)
			if scroll_followers(True):
				print(f"Following all users...")
				followers_of_user(fol)
				follow_all(fol + ".txt")
	elif options == '3':
		usar = input("User which you execute the script: ")
		unfollow_all(usar+"txt")
	elif options == '4':
		if exists("backup.txt"):
			num = input("Place in the publication and select the number of users in each commentary: ")
			mentions("backup.txt", int(num))
		else:
			print(" ")
			print(error + "You have to do a backup first" +  Style.RESET_ALL)
	elif options == '5':
		user1 = input("Select the first user: ")
		user2 = input("Select the second user: ")
		followings_of_user(user1)
		followings_of_user(user2)
		matches(user1,user2)
	elif options == '6':
		backup_of_followers()
	elif options == '7':
		if exists("backup.txt"):
			follow_all("backup.txt")
		else:
			print(" ")
			print(error + "You have to do a backup first" +  Style.RESET_ALL)
	elif options == '8':
		if exists("backup.txt"):
			unfollow_all("backup.txt")
		else:
			print(" ")
			print(error + "You have to do a backup first" +  Style.RESET_ALL)
	elif options == '9':
		print(f"Bye...")
		browser.quit()
		opt = False
	else:
		print(f'Select a valid option')

	print(" ")
	print(alert + "Alert: Don't touch the web, the bot will not work!" + Style.RESET_ALL)