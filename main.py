# encoding: utf-8

from tkinter import *
from tkinter import simpledialog
from keyboard import send as presskey
from functools import partial
import os
import multitasking
import time
import random
import pickle

commandsstorage = []
startstop = False
savepath = 'C:\\Users\\{0}\\Documents\\kol4ikscripts\\buttonbot\\saves\\'.format(os.getlogin())

def addcmnd(srptext, crptext, shdtext, rndtext):
	global commandslb, commandsstorage
	commandsstorage.append([srptext, crptext, shdtext, rndtext])
	commandslb.insert(END, 'Каждые {0} секунд выполняется команда {1} с зажатием в {2} сек. и рандомным разбросом в {3} сек.'.format(srptext, crptext, shdtext, rndtext))

def addcommandbtn():
	global addbutton, commandslb, secondsrepeatble, commandsrepeatble, secondshold, randspread
	srptext, crptext, shdtext, rndtext = secondsrepeatble.get(), commandsrepeatble.get(), secondshold.get(), randspread.get()
	secondsrepeatble.delete(0,END)
	commandsrepeatble.delete(0,END)
	secondshold.delete(0,END)
	randspread.delete(0,END)
	secondshold.insert(0,'1')
	randspread.insert(0,'2')
	addcmnd(srptext, crptext, shdtext, rndtext)

def deletecommand():
	global commandslb, commandsstorage
	commandsstorage.pop(commandslb.curselection()[0])
	commandslb.delete(commandslb.curselection()[0], commandslb.curselection()[0])

def deleteallcommands():
	global commandslb, commandsstorage
	commandsstorage = []
	commandslb.delete(0,END)

def savepatterns():
	global commandsstorage, savepath
	try:
		os.makedirs(savepath)
		print('Создана папка для сохранений')
	except OSError:
		print('Папка уже есть')
	inputname = simpledialog.askstring("Ввод", "Введите название сейва: ", parent=root)
	with open(savepath+inputname+'.dump', 'wb') as file:
		pickle.dump(commandsstorage, file)

def loadsaves(savename):
	global commandsstorage, commandslb, savepath
	deleteallcommands()
	with open(savepath+savename, 'rb') as file:
		for i in pickle.load(file):
			srptext, crptext, shdtext, rndtext = i
			addcmnd(srptext, crptext, shdtext, rndtext)

def deletesaves(savename):
	global savepath
	os.remove(savepath+savename)

def deleteallsaves():
	global savepath
	for i in os.scandir(savepath):
		deletesaves(i.name)

def updatesaves():
	global savepath, savesmenu, loadsaves
	savesmenu.delete(0, END)
	deletesavesmenu.delete(3, END)
	for save in os.listdir(savepath):
		if save.split('.')[-1] == 'dump':
			savesmenu.add_command(label=save, command=partial(loadsaves, save[:]))
			deletesavesmenu.add_command(label=save, command=partial(deletesaves, save[:]))
		else:
			os.remove(savepath+save)

def startstoprptcmd():
	global commandsstorage, startstop
	if startstop == False:
		startstop = True
		for i in commandsstorage:
			repeatcommands(i[0], i[1], i[2], i[3])
	else:
		startstop = False

@multitasking.task
def repeatcommands(secs, buttons, holdsecs, randsecs):
	global startstop
	secs, holdsecs, randsecs = int(secs), int(holdsecs), int(randsecs)
	while startstop:
		presskey(buttons, True, False)
		time.sleep(holdsecs)
		presskey(buttons, False, True)
		time.sleep(random.randint(secs - randsecs, secs + randsecs))

root = Tk()
root.title("Кнопкобот")
root.resizable(False, False)

secondsrepeatble = Entry(root, width=5)
commandsrepeatble = Entry(root, width=15)
commandslb = Listbox(root, height=5, width=95, selectmode=SINGLE)
addbutton = Button(root, text='+', command=addcommandbtn)
startstoprepeating = Button(root, text='Запустить/Остановить', command=startstoprptcmd, justify=CENTER)
secondshold = Entry(root, width=3)
randspread = Entry(root, width=3)

mainmenu = Menu(root)
filemenu = Menu(mainmenu)
savesmenu = Menu(filemenu, postcommand=updatesaves)
deletesavesmenu = Menu(filemenu)
deletesavesmenu.add_command(label='Удалить всё', command=deleteallsaves)
deletesavesmenu.add_separator()
filemenu.add_command(label='Сохранить скрипты', command=savepatterns)
filemenu.add_cascade(label='Загрузить сохры:', menu=savesmenu)
filemenu.add_cascade(label='Удалить сохры:', menu=deletesavesmenu)
mainmenu.add_cascade(label='Файл', menu=filemenu)
root.config(menu=mainmenu)

clearmenu = Menu(tearoff=0)
clearmenu.add_command(label='Удалить выбранное', command=deletecommand)
clearmenu.add_command(label='Очистить всё', command=deleteallcommands)
commandslb.bind('<Button-3>', lambda event: clearmenu.post(event.x_root, event.y_root))

secondshold.insert(END,'1')
randspread.insert(END,'2')

Label(root, text='Каждые ').grid(row=0, column=0)
secondsrepeatble.grid(row=0, column=1)
Label(root, text=' секунд, повторять команды кнопок:').grid(row=0, column=2)
commandsrepeatble.grid(row=0, column=3, padx=5)
Label(root, text='Зажатие -').grid(row=0, column=4)
secondshold.grid(row=0, column=5, padx=5)
Label(root, text='Ранд.раз. -').grid(row=0, column=6)
randspread.grid(row=0, column=7, padx=5)
addbutton.grid(row=0, column=8)
startstoprepeating.grid(row=2, column=3)
commandslb.grid(row=1, column=0, columnspan=8)

root.mainloop()