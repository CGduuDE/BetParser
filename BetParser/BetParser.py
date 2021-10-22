import requests as req
from bs4 import BeautifulSoup as BS
import time
from tkinter import *
from tkinter import messagebox
import re
from urllib import request
from sys import exit
import pymysql

##Created by CGduuDE and j3lly
##
##
##
def xbet():
	all_matches_xbet = []
	url = req.get("https://1xstavka.ru/line/Esports/")
	soup = BS(url.text,"html.parser")

	j = 0
	for row in soup.findAll("div",{"class":"c-events__item c-events__item_col"}): #Ищем блок с инфой о матче

		for link in row.findAll("a",{"class":"c-events__name"}):	
			
			if( not(re.search(r'CSGO',link.get("href"))) ):
				break

			all_matches_xbet.append([])

			for team in row.findAll("span",{"class":"c-events__team"}): #Достаём играющие команды
				regex = re.findall(r'(.+)\s',team.text)
				all_matches_xbet[j].append(regex[0].lower())

			for coef in row.findAll("a",{"class":"c-bets__bet c-bets__bet_coef c-bets__bet_sm"}): #Достаём коэффициенты
				sliced_text = coef.text.split()
				sliced_text = ''.join(sliced_text)
				all_matches_xbet[j].append(sliced_text)

			for time in row.findAll("div",{"class":"c-events__time"}): #Время и дата проведения матча
				regex = re.search(r'\d+[.]\d+',time.text)
				all_matches_xbet[j].append(regex[0])

			j+=1


	for i,item in enumerate(all_matches_xbet):
		if len(all_matches_xbet[i]) == 6 or len(all_matches_xbet[i]) == 3:
			del all_matches_xbet[i]

	return all_matches_xbet

def liga():
	all_matches_liga = []
	url = req.get("https://www.ligastavok.ru/bets/my-line/counter-strike")
	soup = BS(url.text,"html.parser")

	j = 0
	for i in (soup.find_all("div",{"class":"bui-event-row-9eed4e bui-event-row_minimize-28fcc8"})):
		all_matches_liga.append([])

		for team in i.find_all("span",{"class":"bui-commands__command-251fef"}):
			all_matches_liga[j].append(team.text.lower())

		for koef in i.find_all("div",{"class":"bui-group-outcome__default-251771"}): #коэфф.
			if koef.text != '—':
				koef = koef.text
				koef = koef.replace(',', '.')

				koef1 = re.findall(r'\d+[.]\d+',koef)
				all_matches_liga[j].append(koef1[0])
				all_matches_liga[j].append(koef1[1])

		for time in i.find_all("span",{"class":"bui-event-row__time-a6eb59"}):
			all_matches_liga[j].append(time.text)
		j+=1
	return(all_matches_liga)

all_matches_lbet = []
def lbet():
	url = req.get("https://loot3.bet/ru/sport/esports/counter-strike")
	soup = BS(url.text,"html.parser")

	j = 0
	for games in soup.findAll("div",{"class":"match-container ng-star-inserted"}):
		all_matches_lbet.append([])

		for team in games.findAll("span",{"class":"name text-clip"}):
			regex = re.findall(r'\s(.+)',team.text)
			all_matches_lbet[j].append(regex[0].lower())

		for coef in games.findAll("span",{"class":"cof"}):
			all_matches_lbet[j].append(coef.text)

		for time in games.findAll("span",{"class":"time ng-star-inserted"}):
			regex = re.findall(r'[0-9]+',time.text)
			time_hour = int(regex[0]) + 3
			time_all = str(time_hour) + ":" + regex[1]
			all_matches_lbet[j].append(time_all)
		j += 1

	while 0 < len(all_matches_lbet):
		if (len(all_matches_lbet[0]) == 3):
			del all_matches_lbet[0]
		if (len(all_matches_lbet[0]) > 3):
			break


	return all_matches_lbet


def marat():
	live = []
	url = req.get("https://www.marathonbet.ru/su/betting/e-Sports?epcids=all")
	soup = BS(url.text,"html.parser")

	j = 0
	for game in soup.find_all("table",{"class":"coupon-row-item"}):
		live.append([])
		for team in game.find_all("span"):
			live[j].append(team.text.lower())

		j+=1

	for count,i in enumerate(live):
		if live[count][0] == "название события":
			del live[count]
		reg = re.search(r'[+]',live[count][2])
		if reg:
  			del live[count][2]

	return live


def marat_dota():
	live = []
	url = req.get("https://www.marathonbet.ru/su/betting/e-Sports/Dota+2")
	soup = BS(url.text,"html.parser")

	j = 0
	for game in soup.find_all("table",{"class":"coupon-row-item"}):
		live.append([])
		for team in game.find_all("span"):
			live[j].append(team.text.lower())

		j+=1

	for count,i in enumerate(live):
		if live[count][0] == "название события":
			del live[count]
		reg = re.search(r'[+]',live[count][2])
		if reg:
			del live[count][2]

	for count,i in enumerate(live):
		if len(live[count]) > 4:
			del live[count][3]
	return live

def lbet_dota():
	all_matches_lbet = []
	url = req.get("https://loot2.bet/ru/sport/esports/dota-2")
	soup = BS(url.text,"html.parser")

	j = 0
	for games in soup.findAll("div",{"class":"itemNew hover-market"}):
		all_matches_lbet.append([])
		#print(games.text)

		for team in games.findAll("span",{"class":"name text-clip"}):
			regex = re.findall(r'\s(.+)',team.text)
			all_matches_lbet[j].append(regex[0].lower())

		for coef in games.findAll("span",{"class":"cof"}):
			all_matches_lbet[j].append(coef.text)

		for time in games.findAll("span",{"class":"time ng-star-inserted"}):
			regex = re.findall(r'[0-9]+',time.text)
			time_hour = int(regex[0]) + 3
			time_all = str(time_hour) + ":" + regex[1]
			all_matches_lbet[j].append(time_all)
		j += 1

	while 0 < len(all_matches_lbet):
		if (len(all_matches_lbet[0]) == 3):
			del all_matches_lbet[0]
		if (len(all_matches_lbet[0]) > 3):
			break

	for count,i in enumerate(all_matches_lbet):
		if all_matches_lbet[count][1] == 'draw':
			del all_matches_lbet[count][1]


	return all_matches_lbet


nashel = []
def comp(array1,array2, site1, site2):
	for i,item in enumerate(array1):
		for j,item in enumerate(array2):
			if array1[i][0] == array2[j][0] or array1[i][0] == array2[j][1]:
				if array1[i][1] == array2[j][0] or array1[i][1] == array2[j][1]:
					try:
						print("Сайт: " + site1 + ". Матч: " + array1[i][0] + " - " + array1[i][1] + ". Кэфы: " + array1[i][2] + " - " + array1[i][3])
						print("Сайт: " + site2 + ". Матч: " + array2[j][0] + " - " + array2[j][1] + ". Кэфы: " + array2[j][2] + " - " + array2[j][3])
						print('\n')
						var1 = "Сайт: " + site1 + ". Матч: " + array1[i][0] + " - " + array1[i][1] + ". Кэфы: " + array1[i][2] + " - " + array1[i][3] + "\n" + "Сайт: " + site2 + ". Матч: " + array2[j][0] + " - " + array2[j][1] + ". Кэфы: " + array2[j][2] + " - " + array2[j][3] + "\n"
						nashel.append(var1)
						#return var1
						if (float(array1[i][2]) > 2 and float(array2[j][3]) > 2) or (loat(array1[j][2]) > 2 and float(array2[i][3]) > 2):
							print("НАШЕЛ ЕБАА")
							messagebox.showinfo("Error",var1)
							print("Найден матч!: ")
							print("Сайт: " + site1 + ". Матч: " + array1[i][0] + " - " + array1[i][1] + ". Кэфы: " + array1[i][2] + " - " + array1[i][3])
							print("Сайт: " + site2 + ". Матч: " + array2[j][0] + " - " + array2[j][1] + ". Кэфы: " + array2[j][2] + " - " + array2[j][3])
							print("\n")
					except:
						pass


#------------IP PC ---------------------------------
url_ip = req.get("https://2ip.ua/ru/")
soup_ip = BS(url_ip.text,"html.parser")
for i in soup_ip.find_all("div",{"class":"ip"}):
	pc_ip = i.text
	pc_ip = pc_ip.split()
#----------------------------------------------------

def display_full_name():
	#messagebox.showinfo("titiel",name.get() + "" + surname.get())
	global status
	status = 0
	try:
		print("login")
		conn = pymysql.connect(host='localhost', user='root', passwd='', db='users', charset='utf8')
		cursor = conn.cursor()
	
		cursor.execute('SELECT * FROM `login`')

		rows = cursor.fetchall()
	except:
		messagebox.showinfo("Error","No connection to server")

	id = 0
	number_login = 0
	for count,loop in enumerate(rows):
		print(loop[2])
		if loop[2] == name.get():
			number_login = count
			print("login nashel")
			status = 1
			break	
		else:
			status = 0

	for count,loop in enumerate(rows):
		if count == number_login:
			print(loop[3])
			if loop[3] != surname.get():
				messagebox.showinfo("Error","Wrong password or login")
				status = 0
			else:
				status = 1


	for count,loop in enumerate(rows):
		if loop[0] == pc_ip[0]:
			#print("nashel ",count)
			id = count
			break
			
	global days
	if status == 1:
		for a,loop in enumerate(rows):
			if a == number_login:
				print(a,"\t",loop[1])
				days = loop[1]
				if days == 0:
					messagebox.showinfo("Error","Buy a subscription")
					return True

	if status == 1:	
		conn.commit()
		name_label.destroy()
		name_entry.destroy()
		surname_label.destroy()
		surname_entry.destroy()
		message_button.destroy()


def login():
 

	#login = Tk()
	#login.title("GUI на Python")
	global name,surname,name_label,message_button,name_entry,surname_label,surname_entry

	name = StringVar()
	surname = StringVar()
 
	name_label = Label(text="Enter login:",width = 12)
	surname_label = Label(text="Enter password:")
 
	name_label.grid(row=0, column=0, sticky="w")
	surname_label.grid(row=1, column=0, sticky="w")
 
	name_entry = Entry(textvariable=name)
	surname_entry = Entry(textvariable=surname, show = '*')
 
	name_entry.grid(row=0,column=1, padx=5, pady=5)
	surname_entry.grid(row=1,column=1, padx=5, pady=5)
 
 
	message_button = Button(text="login",width=17, height=1, command=display_full_name)
	message_button.grid(row=2,column=1, padx=5, pady=5, sticky="e")



#status = 1
#days = 1
def info():
	messagebox.showinfo("Profile", "days: " + str(days))

#a = input("CS/DOTA: \n")
#if a == "CS":
#print("Анализирую CS:GO\n")
#print("Ищу совпадения...")
#comp(xbet(),lbet(), "xbet", "lootbet")
	#comp(xbet(),liga(), "xbet", "liga")
	#comp(liga(),lbet(), "liga", "lootbet")
	#comp(liga(),marat(), "liga","marat")
#comp(xbet(),marat(), "xbet","marat")
#comp(lbet(),marat(), "lootbet","marat")
#input("Закончил...")

def quit():
    answer = messagebox.askyesno(title="Are you sure?", message="Exit?")
    if answer == True:
        exit()
    else:
    	pass


def cmd_start_csgo():
	try:
		if status == 0:
			messagebox.showinfo("Error","Login")
	except NameError:
		messagebox.showinfo("Error","Login")
	if days == 0:
			messagebox.showinfo("Error","Buy a subscription")
			return True
	if status == 1:
		print("find")
		root.title("Loading...")
		comp(xbet(),lbet(), "xbet", "lootbet")
		comp(xbet(),liga(), "xbet", "liga")
		#comp(liga(),lbet(), "liga", "lootbet")
		comp(liga(),marat(), "liga","marat")
		comp(xbet(),marat(), "xbet","marat")
		#comp(lbet(),marat(), "lootbet","marat")
		global text,scrollbar,languages_listbox
		scrollbar = Scrollbar()
		scrollbar.pack(side=RIGHT, fill=Y)
		text = Text(width=700, height=400,bg="#1A1F28", fg='#0360CB',wrap = WORD)
		text.pack(side=LEFT)
		languages_listbox = Listbox(yscrollcommand=scrollbar.set,width=500, height=400,bg="blue", fg='white')
		for i,a in enumerate(nashel):
			text.insert(1.0, nashel[i] + "\n\n")

		languages_listbox.pack(side=LEFT, fill=BOTH)
		scrollbar.config(command=languages_listbox.yview)
		root.title(pc_ip)

def cmd_start_dota():
	try:
		if status == 0:
			messagebox.showinfo("Error","Login")
	except NameError:
		messagebox.showinfo("Error","Login")
	if days == 0:
			messagebox.showinfo("Error","Buy a subscription")
			return True
	if status == 1:
		print("find")
		root.title("Loading...")
		try:
			comp(lbet_dota(),marat_dota(),"lootbet","marat")
		except:
			messagebox.showinfo("Error","")
			root.title(pc_ip)
			return True
		global text,scrollbar,languages_listbox
		scrollbar = Scrollbar()
		scrollbar.pack(side=RIGHT, fill=Y)
		text = Text(width=700, height=400,bg="#1A1F28", fg='#0360CB', wrap=WORD)
		text.pack(side=LEFT)
		languages_listbox = Listbox(yscrollcommand=scrollbar.set,width=500, height=400,bg="blue", fg='white')
		for i,a in enumerate(nashel):
			text.insert(1.0, nashel[i] + "\n")

		languages_listbox.pack(side=LEFT, fill=BOTH)
		scrollbar.config(command=languages_listbox.yview)
		root.title(pc_ip)



def cmd_clear():
	if True:
		print("clear")
		nashel.clear()
		text.delete('1.0', END)
		languages_listbox.destroy()
		scrollbar.destroy()
		text.destroy()
		pass

def test():
	login()

def developer():
	import webbrowser
	webbrowser.open('https://vk.com/cgduude')
	webbrowser.open('https://vk.com/j3lly')


 
	#login.mainloop()


root = Tk()
root.title(pc_ip)
root.configure(background='#1A1F28')
root.geometry("700x400")
root.resizable(width=False, height=False)
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
#login()
mainmenu = Menu(root) 
root.config(menu=mainmenu) 
 
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="CS:GO",command = cmd_start_csgo)
filemenu.add_command(label="DOTA2",command = cmd_start_dota)
filemenu.add_command(label="FOOTBOOL")
filemenu.add_command(label="clear",command = cmd_clear)


helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="test",command = test)

helpmenu.add_command(label="profile",command = info)
helpmenu.add_command(label="developer",command = developer)

exitmenu = Menu(mainmenu, tearoff=0)
exitmenu.add_command(label="exit",command=quit)

mainmenu.add_cascade(label="GAMES", menu=filemenu)
mainmenu.add_cascade(label="INFO", menu=helpmenu)
mainmenu.add_cascade(label="EXIT", command = quit)
root.mainloop()
#label = Label(text="loading...", fg = "red", bg="black").place(relx=0.5, rely=0.5)

#-----------------BUTTONS-------------------------------
#start = Button(text="CS:GO",
    #bg="black",
    #fg="red",
    #font="Arial 14",
    #command = cmd_start_csgo).place(relx=0.0, rely=0.0)

#clear = Button(text="CLEAR",
  #  bg="black",
   # fg="red",
  ##  font="Arial 14",
   # command = cmd_clear).pack()

#exit1 = Button(text="EXIT",
   # bg="black",
   # fg="red",
   # font="Arial 14",
   # command = quit).place(relx=0.90, rely=0.0)
#--------------------------------------------------------

#if a == "DOTA":
	#print("Анализирую DOTA2")

	#print("Ищу совпадения")

	#comp(lbet_dota(),marat_dota(),"lootbet","marat")

	#input("Закончил")
