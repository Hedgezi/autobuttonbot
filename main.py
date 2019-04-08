# encoding: utf-8

from tkinter import *
from keyboard import send as presskey
import multitasking
import time
import random

commandsstorage = []
startstop = False

def addcommand():
	global addbutton, commandslb, secondsrepeatble, commandsrepeatble, secondshold, randspread
	srptext, crptext, shdtext, rndtext = secondsrepeatble.get(), commandsrepeatble.get(), secondshold.get(), randspread.get()
	secondsrepeatble.delete(0,END)
	commandsrepeatble.delete(0,END)
	secondshold.delete(0,END)
	randspread.delete(0,END)
	secondshold.insert(0,'1')
	randspread.insert(0,'2')
	commandsstorage.append([srptext, crptext, shdtext, rndtext])
	commandslb.insert(END, 'Каждые {0} секунд выполняется команда {1} с зажатием в {2} сек. и рандомным разбросом в {3} сек.'.format(srptext, crptext, shdtext, rndtext))

def deletecommand():
	global commandslb
	commandsstorage.pop(commandslb.curselection()[0])
	commandslb.delete(commandslb.curselection()[0], commandslb.curselection()[0])

def startrepcmd():
	global commandsstorage, startstop
	startstop = True
	for i in commandsstorage:
		repeatcommands(i[0], i[1], i[2], i[3])

def stoprepcmd():
	global startstop
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
addbutton = Button(root, text='Добавить команду', command=addcommand)
deletebutton = Button(root, text='Удалить команду', command=deletecommand)
startrepeating = Button(root, text='Запустить бота', command=startrepcmd)
stoprepeating = Button(root, text='Остановить бота', command=stoprepcmd)
secondshold = Entry(root, width=3)
randspread = Entry(root, width=3)

secondshold.insert(END,'1')
randspread.insert(END,'2')

Label(root, text='Каждые ').grid(row=0, column=0)
secondsrepeatble.grid(row=0, column=1)
Label(root, text=' секунд, повторять команды кнопок:').grid(row=0, column=2)
commandsrepeatble.grid(row=0, column=3)
Label(root, text='Зажатие -').grid(row=0, column=4)
secondshold.grid(row=0, column=5, padx=5)
Label(root, text='Ранд.раз. -').grid(row=0, column=6)
randspread.grid(row=0, column=7, padx=5)
addbutton.grid(row=0, column=8)
deletebutton.grid(row=1, column=8)
startrepeating.grid(row=2, column=2)
stoprepeating.grid(row=2, column=3)
commandslb.grid(row=1, column=0, columnspan=8)

root.mainloop()