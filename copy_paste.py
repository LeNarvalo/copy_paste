from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.keyboard import Controller
from pygame.mixer import music
import threading, win32clipboard, win32gui, time, string, win32api, os, pygame, sys, tooltip
from tkinter import *
from tkinter.colorchooser import askcolor 
from tkinter import PhotoImage as PI

pygame.init()

'''RESTE A FAIRE'''
#Bring fenetre d'aide Ctrl+v+? par dessus

#####################VARIABLES######################
chemin = os.path.expanduser('~\Copy_Paste')
parameters=[1,1,0,44,"#02f131","#02e6f1"]
arg=''
words=[]
number_c=[""]
number_v=""
num_pad = ['<96>','<97>','<98>','<99>','<100>','<101>','<102>','<103>','<104>','<105>']
start_audio = 0
pos_audio = 0
tip_time=time.time()
type=None
listener=None
passed=False
paste_finished=False #Useless
####################################################

if not os.path.exists(chemin):  
	win32api.MessageBox(0, 'Vous devez réinstaller copy_past !', 'Fichiers manquants', 0x00040030)
	sys.exit(1)

try:
	file = open(chemin+"\\Params.txt","r")
	p = file.readlines()
	file.close()
	parameters=[int(p[0]),int(p[1]),int(p[2]),int(p[3]),p[4][:-1],p[5]]

except:
	file = open(chemin+"\\Params.txt","w")
	file.writelines(['1','\n','1','\n','0','\n','44','\n',"#02f131",'\n',"#02e6f1"])
	file.close()

def launch_listener():
	global listener
	with Listener(on_release=on_release) as listener:
		listener.join()

def playsound(action):
	if not parameters[0]:
		return

	music.set_volume(1)
	try:
		music.load(chemin+"\\"+action+".mp3")
		music.play()
	except:
		music.load(chemin+"\\"+action+".ogg")
		music.play(loops=-1,start=pos_audio)

def pop_up(action,num,t1,t2):
	global root, txt, lbl
	#x,y=win32gui.GetCursorPos()
	if not parameters[1]:
		return

	displayed=False
	if win.state()!="withdrawn":
		win.withdraw()
		calcul_pos_audio()
		displayed=True

	if action == "Ctrl + C":
		lbl.configure(fg=parameters[4])
	else:
		lbl.configure(fg=parameters[5])
	time.sleep(t1)
	root.deiconify()
	root.attributes("-topmost", True)
	txt.set(action)
	root.update()
	# Gets the requested values of the height and widht.
	windowWidth = root.winfo_reqwidth()
	windowHeight = root.winfo_reqheight()
	# Gets both half the screen width/height and window width/height
	positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
	root.geometry("+{}+{}".format(positionRight, positionDown))
	time.sleep(t2)
	root.withdraw()

	root.deiconify()
	root.attributes("-topmost", True)
	txt.set(num)
	root.update()
	# Gets the requested values of the height and widht.
	windowWidth = root.winfo_reqwidth()
	windowHeight = root.winfo_reqheight()
	# Gets both half the screen width/height and window width/height
	positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
	root.geometry("+{}+{}".format(positionRight, positionDown))
	time.sleep(0.5)
	root.withdraw()
	if action == "Ctrl + V":
		return #Je n'arrive pas à réouvrir la fenêtre d'options uniquement quand l'auto-suppression est finie...
	if displayed:
		threading.Thread(target=playsound,args=("Eric Skiff - Arpanauts",)).start()
		win.deiconify()

def root_tk():
	global root, txt,lbl
	root = Tk()
	root.overrideredirect(True)
	txt = StringVar()
	lbl = Label(textvariable=txt,justify='center',font = "fixedsys "+str(parameters[3])+" bold")
	lbl.pack()
	check_color(parameters[4],parameters[5])
	root.withdraw()
	root.mainloop()

def check_color(color,other_param):
	for c in ["#7e7e7e","#ffffff","#000000"]:
		if c != color  and c != other_param :
			lbl.configure(bg=c)
			root.wm_attributes('-transparentcolor',c)
			return

def choose_color_c(event=1):
	global parameters, root
	frame1a.configure(relief=SUNKEN)
	frame1.update()
	# variable to store hexadecimal code of color
	color = askcolor(title ="Choississez la couleur")[1]
	if color is not None:
		parameters[4] = color
	else:
		frame1a.configure(relief=RAISED)
		frame1.update()
		return

	check_color(color,parameters[5])


	file = open(chemin+"\\Params.txt","w")
	file.writelines([str(parameters[0]),'\n',str(parameters[1]),'\n',str(parameters[2]),'\n',str(parameters[3]),'\n',str(parameters[4]),'\n',str(parameters[5])])
	file.close()
	ex_label1.configure(fg=parameters[4])
	l1.configure(fg=parameters[4])
	frame1a.configure(relief=RAISED)
	frame1.update()

def choose_color_v(event=1):
	global parameters
	frame1b.configure(relief=SUNKEN)
	frame1.update()
	# variable to store hexadecimal code of color
	color = askcolor(title ="Choississez la couleur")[1]
	if color is not None:
		parameters[4] = color
	else:
		frame1b.configure(relief=RAISED)
		frame1.update()
		return

	check_color(color,parameters[3])
	
	file = open(chemin+"\\Params.txt","w")
	file.writelines([str(parameters[0]),'\n',str(parameters[1]),'\n',str(parameters[2]),'\n',str(parameters[3]),'\n',str(parameters[4]),'\n',str(parameters[5])])
	file.close()
	ex_label2.configure(fg=parameters[4])
	l2.configure(fg=parameters[4])
	frame1b.configure(relief=RAISED)
	frame1.update()

def calcul_pos_audio():
	global pos_audio,start_audio

	pos_audio=int(time.time())-start_audio
	if pos_audio > 196:
		pos_audio=(int(time.time())-start_audio)-int((time.time()-start_audio)/196)*196
		start_audio=int(time.time())-pos_audio
	print("pos_audio :",pos_audio)

def set_parameters(event):
	global parameters
	if event.widget.cget('text') == "Sons":
		parameters[0]=1-parameters[0]
		if parameters[0]:
			threading.Thread(target=playsound,args=("copy",)).start()

	elif event.widget.cget('text') == "Animations visuelles":
		parameters[1]=1-parameters[1]
		if parameters[1]:
			threading.Thread(target=playsound,args=("copy",)).start()
			threading.Thread(target=pop_up,args=("Ctrl + C",str(42),0.1,0.5,)).start()

	elif event.widget.cget('text') == "Auto-suppression":
		parameters[2]=1-parameters[2]

	file = open(chemin+"\\Params.txt","w")
	file.writelines([str(parameters[0]),'\n',str(parameters[1]),'\n',str(parameters[2]),'\n',str(parameters[3]),'\n',str(parameters[4]),'\n',str(parameters[5])])
	file.close()

def on_closing():
	win.withdraw()
	while music.get_volume()>0.1:
		try:
			music.set_volume(music.get_volume()-0.1)
			time.sleep(0.15)
		except:
			print("BUG SOUND")
	calcul_pos_audio()
	music.stop()

def options():
	global win, fontsize, ft_size_label, s, ex_label1, ex_label2, win, frame1a, frame1b, l1, l2, frame1
	win = Tk()
	win.protocol("WM_DELETE_WINDOW", on_closing)
	win.title("Paramètres du Presse-Papiers")
	win.configure(bg="white")

	win.p1=PI(master = win,file = chemin+"\\color.png")

	file = open(chemin+"\\Params.txt","r")
	p = file.readlines()
	file.close()
	parameters=[int(p[0]),int(p[1]),int(p[2]),int(p[3]),p[4][:-1],p[5]]

	frame0 = Frame(win,bg="white")
	frame0.grid(row=0,column=0,columnspan=3)
	col=0
	for arg in list(zip(["Sons","Animations visuelles","Auto-suppression"],parameters)):
		c=Checkbutton(frame0, text = arg[0],bg="white")
		c.bind("<ButtonRelease-1>", set_parameters)
		c.grid(row=0,column=col,sticky='w',padx=50,pady=10)
		if arg[1]:
			c.select()
		else:
			c.deselect()
		if arg[0] == "Auto-suppression":
			tooltip.register(c, "Supprime automatique le texte collé et le numéro saisi")
		col+=1

	frame1 = Frame(win,bg="white")
	frame1.grid(row=1,column=0,columnspan=3,pady=10)
	frame1a = Frame(frame1,bd=2,relief=RAISED)
	frame1a.grid(row=0,column=0,padx=50)
	button1 = Button(frame1a, image=win.p1, command = choose_color_c,bd=0)
	button1.pack(side=LEFT)
	l1 = Label(frame1a,text="Couleur Ctrl+C",fg=parameters[4])
	l1.pack(side=RIGHT,padx=15)
	l1.bind("<ButtonRelease-1>",choose_color_c)
	frame1a.bind("<ButtonRelease-1>",choose_color_c)

	frame1b = Frame(frame1,bd=2,relief=RAISED)
	frame1b.grid(row=0,column=1,padx=50)
	button2 = Button(frame1b, image=win.p1, command = choose_color_v, bd=0)
	button2.pack(side=LEFT)
	l2 =Label(frame1b,text="Couleur Ctrl+V",fg=parameters[5])
	l2.pack(side=RIGHT,padx=15)
	l2.bind("<ButtonRelease-1>",choose_color_v)
	frame1b.bind("<ButtonRelease-1>",choose_color_v)

	label_ft = Label(win, text = "Font Size : ",bg="white")
	label_ft.grid(row=2,column=0,sticky='w',pady=10)
	label_ft.grid_propagate(0)

	s = Scale(win, from_ = 8, to = 84, orient = HORIZONTAL,showvalue=False,length=550,bg="white")
	s.bind("<Motion>", set_fontsize)
	s.set(parameters[3])
	s.grid(row=2,column=1,sticky='w')
	s.grid_propagate(0)

	ft_size_label = Label(win, text = str((3-len(str(s.get())))*"0"+str(s.get())),bg="white")
	ft_size_label.grid(row=2,column=2,sticky='w')
	ft_size_label.grid_propagate(0)

	frame2 = Frame(win,bg="white")
	frame2.grid(row=3,column=0,columnspan=3)
	frame2.grid_propagate(0)
	win.columnconfigure(1, weight=1)
	ex_label1 = Label(frame2, text = "Copier", font = "fixedsys "+str(parameters[3])+" bold", fg=parameters[4],bg="white")
	ex_label1.pack()

	ex_label2 = Label(frame2, text = "Coller", font = "fixedsys "+str(parameters[3])+" bold", fg=parameters[5],bg="white")
	ex_label2.pack()
	win.withdraw()
	win.mainloop()

def get_parameters():
	global parameters, fontsize, ft_size_label, s, ex_label1, ex_label2, win, photo1, start_audio
	win.deiconify()
	win.attributes("-topmost", True)
	if not start_audio:
		start_audio=int(time.time())

	threading.Thread(target=playsound,args=("Eric Skiff - Arpanauts",)).start()
	# Gets both half the screen width/height and window width/height
	positionRight = int(win.winfo_screenwidth()/2 - 650/2)
	positionDown = int(win.winfo_screenheight()/2 - 640/2)
	win.geometry("+{}+{}".format(positionRight, positionDown))

def set_fontsize(event):
	global parameters
	lbl.configure(font="fixedsys "+str(s.get())+" bold")
	parameters[3]=s.get()
	ft_size_label.configure(text=str((3-len(str(parameters[3])))*"0"+str(parameters[3])))
	ex_label1.configure(font="fixedsys "+str(s.get())+" bold")
	ex_label2.configure(font="fixedsys "+str(s.get())+" bold")
	file = open(chemin+"\\Params.txt","w")
	file.writelines([str(parameters[0]),'\n',str(parameters[1]),'\n',str(parameters[2]),'\n',str(parameters[3]),'\n',str(parameters[4]),'\n',str(parameters[5])])
	file.close()

def copy_fx():
	global type, passed
	type=None
	if number_c[-1]:
		#print('ctrl+c+n°',number_c[-1])
		while number_c.count(number_c[-1])>1:
			id = number_c.index(number_c[-1])
			del words[id]
			number_c.remove(number_c[-1])
		win32clipboard.OpenClipboard()
		word = win32clipboard.GetClipboardData()
		win32clipboard.CloseClipboard()
		words.append(word)
		threading.Thread(target=playsound,args=("copy",)).start()
		threading.Thread(target=pop_up,args=("Ctrl + C",str(number_c[-1]),0.1,0.5,)).start()
		#print(list(zip(number_c,words)))
		number_c.append("")
	passed=True
	listener.stop()
	return False

def paste_fx():
	global type, passed
	type=None
	#paste_finished=False
	passed=True
	if number_v in number_c and number_v:
		nv=number_v #permet d'éviter la remise à None de number_v sur un autre thread
		threading.Thread(target=playsound,args=("paste",)).start()
		threading.Thread(target=pop_up,args=("Ctrl + V",str(nv),0.068,0.45,)).start()
		time.sleep(1)
		k = Controller()
		try:
			win32clipboard.OpenClipboard()
			word = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
		except:
			word=""
		if parameters[2]:
			try:
				for l in word+nv:
					k.press(Key.backspace)
					k.release(Key.backspace)
			except:
				pass
		word = words[number_c.index(nv)]
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardText(word)
		win32clipboard.CloseClipboard()
		k.press(Key.ctrl_l)
		k.press('v')
		k.release(Key.ctrl_l)
		k.release('v')
		listener.stop()		
		return False
	
	else:
		listener.stop()
		return False

def test_tip_numpad():
	while 1:
		if time.time()-tip_time>1.5 and type=="copy":
			copy_fx()
		elif time.time()-tip_time>1.5 and type=="paste":
			paste_fx()
		time.sleep(0.10)

def on_release(key):
	global number_c, license, number_v, passed, listener, tip_time, type
	try:
		exit = key.char
		if exit=="?":
			help_text=""
			for c in list(zip(number_c,words)):
				if len(c[1])>=25:
					help_text+=c[0]+' : '+c[1][:40]+"...\n"
				else:
					help_text+=c[0]+' : '+c[1][:40]+"\n"
			win32api.MessageBox(0, help_text, 'Presse-papiers', 0x00010040)
			listener.stop()
			return False

		elif exit=="!":
			threading.Thread(target=get_parameters).start()
			listener.stop()
			return False

		if arg=='c':
			if str(key) in num_pad:
				number_c[-1]+=str(num_pad.index(str(key)))
				type="copy"
				tip_time=time.time()

			elif exit != 'c' and exit in string.printable :
				#print('not c :',key, exit)
				listener.stop()
				return False

		elif arg=='v':
			if str(key) in num_pad :
				number_v+=str(num_pad.index(str(key)))
				type="paste"
				tip_time=time.time()

			elif exit != 'v' and exit in string.printable :
				listener.stop()
				return False
	except:
		try:
			if key.name == "ctrl_l":
				if not passed:
					passed=True
	
				else:
					if arg=='c':
						copy_fx()
		
					elif arg=='v':
						paste_fx()

			else:
				listener.stop()
				return False

		except:
			print('bug')
			return False

def ctrl_c_or_v():
	global passed
	passed=False
	try:
		listener.stop()
	except:
		pass
	threading.Thread(target=launch_listener).start()

def ctrl_c():
	global arg
	arg='c'
	ctrl_c_or_v()

def ctrl_v():
	global arg, number_v
	arg='v'
	number_v = ''
	ctrl_c_or_v()

threading.Thread(target=root_tk).start()
threading.Thread(target=options).start()
threading.Thread(target=test_tip_numpad).start()
with keyboard.GlobalHotKeys({
		'<ctrl>+c': ctrl_c,
		'<ctrl>+v': ctrl_v,
		}) as h:
	h.join()
