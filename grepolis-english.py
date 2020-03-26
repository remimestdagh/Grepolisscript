from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
from random import randint
from selenium.webdriver.chrome.options import Options


###############
#SETTING UP THINGS
###############
url = "https://nl.grepolis.com/"
print('################ GREPOLIS  BOT')
username = "HenkHamster"#input('Username: ')
password = "apenkool8"#input('Password: ')
selected_town = "Stad van HenkHamster" #input("City name( 0 to don't select a main city ): ")
towns_number = int(input('Number of cities: '))
world_number = int(input('World number: '))



##############
#INITIALIZARI
##############


building_names_english = ["Senate", "Cave", "Timber Camp", "Quarry", "Silver Mine", "Marketplace", "Harbor", "Barracks", "City Wall", "Warehouse", "Farm", "Academy", "Temple", "Terme", "Torre"]
building_names = ["main", "hide", "lumber", "stoner", "ironer", "market", "docks", "barraks", "wall", "storage", "farm", "academy", "temple", "terme", "torre"]

matrix_buildings_real = [[0 for i in range(15)] for i in range(towns_number)]

wood = 0
stone = 0
silver = 0
pop = 0

matrix_buildings = [
	[17, 10, 25, 25, 25, 10, 15, 10, 20, 25, 45, 30, 17, 0, 0],

	[17, 10, 20, 20, 21, 10, 15, 10, 20, 25, 45, 30, 17, 0, 0],

	[17, 10, 20, 20, 21, 10, 15, 10, 20, 25, 45, 30, 17, 0, 1],
]


err_senate = False



def rand_time():
	return (0.5 + randint(0, 15)/10)


def get_city_name(br):
	try:
		name = br.find_element_by_css_selector(".town_name").text
		return name
	except:
		print("Name of the city could not be found.")
		enter_world(br)



def next_town(br):
	try:
		search = br.find_element_by_css_selector(".btn_next_town")
		search.click()
		search = br.find_element_by_css_selector(".btn_jump_to_town")
		search.click()
		print(get_city_name(br))
		print("The city has been changed.")
		time.sleep(rand_time())
	except:
		print("Impossible to change city.")
		time.sleep(2)



def find_town(br):
	while(True):
		if(get_city_name(br) == selected_town or selected_town == '0'):
			print("City found.")
			break
		else:
			next_town(br)

def enter_world(br):
	try:
		search = br.find_elements_by_css_selector(".world_name")
		a = 0
		for i in search:
			if(a == world_number-1):#NUMERO DEL MONDO CHE COMPARE IN ORDINE NELLA SCHERMATA DOPO LOGIN
				i.click()
			a += 1
	except:
		print("Starting game error..\nRetrying..")
		time.sleep(5)
		enter_world(br)


def login(br):
	try:
		#To fill out a form    ui-button-text
		search = br.find_element_by_name('login[userid]')
		search.send_keys(username)
		search = br.find_element_by_name('login[password]')
		search.send_keys(password)
		search = br.find_element_by_name("login[Login]")
		search.send_keys(Keys.RETURN)
		time.sleep(5)
	except:
		print("Autentification error..")
		time.sleep(5)
		login(br)


def bonus_collector(br):
	try:
		search = br.find_element_by_css_selector(".js-tooltip-resources")
		search.click()
		time.sleep(5)
	except:
		print("Daily bonus not available.")


def view_town(br):
	try:
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		search = br.find_element_by_css_selector(".city_overview div")
		search.click()
		print("The City is being inspected.")
		time.sleep(2)
	except:
		print("Inspecting city failed.")

def view_island(br):
	try:
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		search = br.find_element_by_css_selector(".island_view div")
		search.click()
		search = br.find_element_by_css_selector(".btn_jump_to_town div")
		search.click()
		print("The Island is being inspected.")
	except:
		print("Inspecting Island failed.")
	time.sleep(4)


def get_town_info(br):
	try:
			global wood
			wood = br.find_element_by_css_selector(".ui_resources_bar .wood .amount").text
			global stone
			stone = br.find_element_by_css_selector(".ui_resources_bar .stone .amount").text
			global silver
			silver = br.find_element_by_css_selector(".ui_resources_bar .iron .amount").text
			global pop
			pop = br.find_element_by_css_selector(".ui_resources_bar .population .amount").text
			print("City informations:\n Wood: " + wood + " | Stone: "  + stone + " | Silver: "  + silver + " | Population: "  + pop + " " )
	except:
		print("Impossible to find city resources!")
def attack_bandit(br):
	try:
		bandit = br.find_element_by_css_selector(".attack_spot.attack_possible")
		bandit.click()
		time.sleep(2)
		allUnits = br.find_element_by_css_selector(".select_all")
		allUnits.click()
		time.sleep(2)
		attackButton = br.find_element_by_css_selector(".button_new.double_border .caption")
		attackButton.click()
		time.sleep(2)


	except:
		print("Can't attack bandit")
def collect_reward(br):
	try:
		reward = br.find_element_by_css_selector(".attack_spot.collect_reward")
		reward.click()
		time.sleep(2)
		button = br.find_element_by_css_selector(".cover_parent")
		button.click()
		time.sleep(1)
		#useNow = br.find_element_by_css_selector(".context_icon#item_reward_use")
		#useNow.click()
		stash = br.find_element_by_css_selector(".context_icon#item_reward_stash")
		stash.click()
		time.sleep(1)
	except:
		print("No reward")
def speed_construction(br):
	try:
		
		free2 = br.find_element_by_css_selector(".button_new.instant_buy")
		free2.click()
		time.sleep(5)
		free3 = br.find_element_by_css_selector(".button_new.instant_buy")
		free3.click()
		print("Building list accelerated.")
		time.sleep(3)
	except:
		print("Can't accelerate building list.")

def get_population(br):
	if int(pop) <= 20:
		print("Attention, population is very low!")
		br.execute_script("BuildingMain.buildBuilding('farm', 20);")

	time.sleep(2)

def check_buildings(br):
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	try:
		senate = br.find_element_by_xpath("//*[@id='building_main_area_main']")
		senate.click()
		print("The Senate is being inspected.")
		err_senate = False
		time.sleep(2)
	except:
		print("Senate inspecting is not available.")
		err_senate = True


	if(err_senate==False):
		buildings = br.find_elements_by_css_selector(".white")
		count_buildings = 0
		for build in buildings:
			matrix_buildings_real[n_city][count_buildings] = int(build.text)
			count_buildings += 1

		print (matrix_buildings[n_city])
		print (matrix_buildings_real[n_city])

		for num_building in range(0, 13):
			real = matrix_buildings_real[n_city][num_building]
			ideal = matrix_buildings[n_city][num_building]
			if(real < ideal):
				print("Building "+ building_names_english[num_building] +" underleveled by %d levels" % (ideal-real))
				comando_up = "BuildingMain.buildBuilding('"+building_names[num_building]+"', 50);"
				br.execute_script(comando_up)
	webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
	print("Finished upgrading buildings.")
	time.sleep(5)

def collect_resources(br):
	villages = br.find_elements_by_xpath("//*[@data-same_island='true']")
	print("Found %d villages." % len(villages))
	i = 0
	for village in villages:
		print("I act in the village: " + str(i + 1))
		webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		time.sleep(rand_time()+1)
		search = br.find_elements_by_xpath("//*[@data-same_island='true']") #.owned
		a = -1
		for sc in search:
			a += 1
			if(a == i):
				try:
					sc.click()
				except:
					print("Can't open village panel.")
				time.sleep(rand_time())
				try:
					ele = br.find_element_by_css_selector(".card_click_area")
					ele.click()
				except:
					print("Can't collet resources from village.")
				time.sleep(rand_time())
				webdriver.ActionChains(br).send_keys(Keys.ESCAPE).perform()
		i += 1
		time.sleep(rand_time())


def footer(br):
	end = time.time()
	print("Duration: " + str(int(end - start)) + " seconds")

	waiting_time = TEMPO - (int(end - start))*0.80
	if(waiting_time < 5):
			waiting_time = 5

	random_time = rand_time()*3.14+rand_time()*7/5 +rand_time()*19/7+20
	wait_time = int(waiting_time) + int(random_time)
	print("Next cycle in " + str(wait_time) + " seconds")
	y = 0.05
	z = 0
	for i in range(0, wait_time):
		if wait_time - int(wait_time*y) == wait_time - i:
			z+= 1
			y+= 0.05
		percent_done = 100 - int((wait_time - i)/wait_time * 100)
		
		

		time.sleep(1)
	print("-------------------------------------------------------------\n-------------------------------------------------------------\n")












TEMPO = 300    # 5 minute de pauza intre cicluri
#br = webdriver.Chrome()



#options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir=/home/kinder/.config/google-chrome") #Path to your chrome profile
br = webdriver.Chrome(executable_path="chromedriver.exe")




#start it up
print("Oppening up Chrome....")
br.get(url)
time.sleep(3)


login(br)
enter_world(br)
bonus_collector(br)

while(True):
	try:
		enter_world(br)
		find_town(br)
		start = time.time()
		
		for n_city in range(0, towns_number):


			print("Working in the city: "+get_city_name(br))

			view_town(br)
			get_town_info(br)
			speed_construction(br)
			get_population(br)
			
			#check_buildings(br)

			view_island(br)
			collect_reward(br)
			attack_bandit(br)
			collect_resources(br)

			next_town(br)


		footer(br)
	except:
		print("BOT ERROR!!!")
		br.get(url)
		login(br)
		time.sleep(30)
