# encoding: utf-8

from tkinter import *
from keyboard import send as presskey
import multitasking
import time
import random

commandsstorage = []
startstop = False

def addcommand():
	global addbutton, commandslb, secondsrepeatble, commandsrepeatble, secondshold
	srptext, crptext, shdtext = secondsrepeatble.get(), commandsrepeatble.get(), secondshold.get()
	secondsrepeatble.delete(0,END)
	commandsrepeatble.delete(0,END)
	secondshold.delete(0,END)
	commandsstorage.append([srptext, crptext, shdtext])
	commandslb.insert(END, 'Каждые {0} секунд выполняется команда {1} с зажимом в {2} сек.'.format(srptext, crptext, shdtext))

def deletecommand():
	global commandslb
	commandsstorage.pop(commandslb.curselection()[0])
	commandslb.delete(commandslb.curselection()[0], commandslb.curselection()[0])

def startrepcmd():
	global commandsstorage, startstop
	startstop = True
	for i in commandsstorage:
		repeatcommands(i[0], i[1], i[2])

def stoprepcmd():
	global startstop
	startstop = False

@multitasking.task
def repeatcommands(secs, buttons, holdsecs):
	global startstop
	secs, holdsecs = int(secs), int(holdsecs)
	while startstop:
		presskey(buttons, True, False)
		time.sleep(holdsecs)
		presskey(buttons, False, True)
		time.sleep(random.randint(secs - 2, secs + 2))

root = Tk()
root.title("Кнопкобот")
root.resizable(False, False)

secondsrepeatble = Entry(root, width=5)
commandsrepeatble = Entry(root, width=15)
commandslb = Listbox(root, height=5, width=70, selectmode=SINGLE)
addbutton = Button(root, text='Добавить команду', command=addcommand)
deletebutton = Button(root, text='Удалить команду', command=deletecommand)
startrepeating = Button(root, text='Запустить бота', command=startrepcmd)
stoprepeating = Button(root, text='Остановить бота', command=stoprepcmd)
secondshold = Entry(root, width=3)

secondshold.insert(END,'1')

Label(root, text='Каждые ').grid(row=0, column=0)
secondsrepeatble.grid(row=0, column=1)
Label(root, text=' секунд, повторять команды кнопок:').grid(row=0, column=2)
commandsrepeatble.grid(row=0, column=3)
Label(root, text='-').grid(row=0, column=4)
secondshold.grid(row=0, column=5, padx=5)
addbutton.grid(row=0, column=6)
deletebutton.grid(row=1, column=6)
startrepeating.grid(row=2, column=2)
stoprepeating.grid(row=2, column=3)
commandslb.grid(row=1, column=0, columnspan=6)

root.mainloop()