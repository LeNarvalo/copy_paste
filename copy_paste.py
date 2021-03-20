import keyboard as KEYBOARD
from pynput import keyboard
from pynput.keyboard import Key, Listener
from pygame.mixer import music
from tkinter import *
import tkinter.ttk  as ttk
from tkinter.colorchooser import askcolor 
from tkinter import PhotoImage as PI
from PIL import ImageGrab, Image
from match_img import find_match, thread_match
from run_array import Spiral, Methodic
from win32api import GetSystemMetrics, GetMonitorInfo, MonitorFromPoint
#from memory_profiler import profile
import threading, clipboard, win32gui, time, string, win32api, os, pygame, sys, tooltip, ctypes, win32con, winsound, cv2, math, reeval

pygame.init()

'''RESTE A FAIRE'''
#Vérifier si les bords noirs sont moins long à analyser que les images avec des détails
#Créer une fonction pour réévaluer
#Rogner l'image précédente pour ne conserver que les bords
'''____END______'''

#####################VARIABLES######################
chemin = os.path.expanduser('~\Copy_Paste')
parameters =[0,0,44,"#02f131",0.80,2,0]
words = []
number_c = ["-1"]
number_v = ""
num_pad = ['<96>','<97>','<98>','<99>','<100>','<101>','<102>','<103>','<104>','<105>']
start_audio = 0
pos_audio = 0
tip_time = time.time()+time.time()
listener = None
passed = 0
shift_pressed = False
option_pressed = False
screens = []
pcd_screens = []
min_coords = (0,0)
running = False
popupisation = False
####################################################

def getpid(process_name):
	return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()]

current_pid = os.getpid()
process_pid = getpid("copy_paste.exe")
for pid in process_pid:
	if int(pid) != current_pid:
		os.kill(int(pid),21)

if not os.path.exists(chemin):  
    win32api.MessageBox(0, 'Vous devez réinstaller copy_past !', 'Fichiers manquants', 0x00040030)
    sys.exit(1)

if not os.path.exists(chemin+"\\Screenshots"):  
    os.mkdir(chemin+"\\Screenshots")
    #os.mkdir(chemin+"\\Screenshots\\Crops")

try:
    file = open(chemin+"\\Params.txt","r")
    p = file.readlines()
    file.close()
    parameters=[int(p[0]),int(p[1]),int(p[2]),p[3][:-1],float(p[4]),int(p[5]),int(p[6])]

except:
    file = open(chemin+"\\Params.txt","w")
    file.writelines(['0','\n','0','\n','44','\n',"#02f131",'\n','0.80','\n','2','\n','0'])
    file.close()

def launch_listener():
    global listener
    with Listener(on_release=on_Release) as listener:
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
    global root, txt, lbl, popupisation
    #x,y=win32gui.GetCursorPos()
    if not parameters[1]:
        return

    popupisation = True
    displayed=False
    if win.state() == 'normal':
        displayed=True
        threading.Thread(target=on_closing,args=(True,)).start()

    lbl.configure(fg=parameters[3])
    time.sleep(t1)
    root.deiconify()
    root.attributes("-topmost", True)
    txt.set(action)
    root.update()
    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    size = GetMonitorInfo(MonitorFromPoint((0,0))).get('Work')
    height = size[3]+size[1]
    width = size[2]+size[0]
    positionDown = int(height/2 - windowHeight/2)
    positionRight = int(width/2 - windowWidth/2)
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
    positionDown = int(height/2 - windowHeight/2)
    positionRight = int(width/2 - windowWidth/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    time.sleep(0.5)
    root.withdraw()

    popupisation = False

    #if action == "Ctrl + V":
    #    return #Je n'arrive pas à réouvrir la fenêtre d'options uniquement quand l'auto-suppression est finie...

    if displayed:
        win.deiconify()
        threading.Thread(target=playsound,args=("Eric Skiff - Arpanauts",)).start()

def root_tk():
    global root, txt, lbl
    root = Tk()
    root.overrideredirect(True)
    txt = StringVar()
    lbl = Label(textvariable=txt,justify='center',font = "fixedsys "+str(parameters[2])+" bold")
    lbl.pack()
    check_color(parameters[3])
    root.withdraw()
    root.mainloop()

def check_color(color):
    for c in ["#7e7e7e","#ffffff","#000000"]:
        if c != color :
            lbl.configure(bg=c)
            root.wm_attributes('-transparentcolor',c)
            return

def choose_color_v(event=1):
    global parameters
    frame1b.configure(relief=SUNKEN)
    frame1.update()
    # variable to store hexadecimal code of color
    color = askcolor(title ="Choississez la couleur")[1]
    if color is not None:
        parameters[3] = color
    else:
        frame1b.configure(relief=RAISED)
        frame1.update()
        return

    check_color(color,parameters[2])
    
    write_parameters()
    
    ex_label2.configure(fg=parameters[3])
    l2.configure(fg=parameters[3])
    frame1b.configure(relief=RAISED)
    frame1.update()

def calcul_pos_audio():
    global pos_audio,start_audio

    pos_audio=int(time.time())-start_audio
    if pos_audio > 196:
        pos_audio=(int(time.time())-start_audio)-int((time.time()-start_audio)/196)*196
        start_audio=int(time.time())-pos_audio

def set_parameters(event):
    global parameters
    if event.widget.cget('text') == "Sons":
        parameters[0]=1-parameters[0]        
        if parameters[0]:
            threading.Thread(target=playsound,args=("Eric Skiff - Arpanauts",)).start()
        else:
            calcul_pos_audio()
            music.stop()

    elif event.widget.cget('text') == "Animations visuelles":
        parameters[1]=1-parameters[1]
        if parameters[1]:
            threading.Thread(target=playsound,args=("paste",)).start()
            threading.Thread(target=pop_up,args=("Ctrl + V",str(42),0.1,0.5,)).start()

    elif event.widget.cget('text') == "Auto-suppression":
        parameters[6]=1-parameters[6]

    write_parameters()

def write_parameters():
    file = open(chemin+"\\Params.txt","w")
    file.writelines([str(parameters[0]),'\n',str(parameters[1]),'\n',str(parameters[2]),'\n',str(parameters[3]),'\n',str(parameters[4]),'\n',str(parameters[5]),'\n',str(parameters[6])])
    file.close()

def OnUnmap(event):
    if not popupisation:
        on_closing()

def on_closing(only_win=False):
    win.withdraw()
    if not only_win:
        his.withdraw()
    while music.get_volume()>0.1:
        try:
            vol = music.get_volume()-0.1
            music.set_volume(vol)
            time.sleep(0.15)
            if music.get_volume()> vol: #Pour le menu option
                calcul_pos_audio()
                return
        except:
            print("BUG SOUND")
    calcul_pos_audio()
    music.stop()

def get_threshold(event=None):
    global parameters
    parameters[4] = sp1.get()
    write_parameters()
    
def get_min_match(event=None):
    global parameters
    parameters[5] = sp2.get()
    write_parameters()

def lch_reeval(event=1):
    frame1c.configure(relief=SUNKEN)
    frame1.update()
    threading.Thread(target=reeval.widget,args=(parameters[4],parameters[5],)).start()
    win.withdraw()
    time.sleep(0.25)
    frame1c.configure(relief=RAISED)
    frame1.update()

def options():
    global win, fontsize, ft_size_label, s, ex_label2, win, frame1a, frame1b, l1, l2, frame1, sp1, sp2, frame1c
    win = Tk()
    win.resizable(0,0)
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.bind("<Unmap>", OnUnmap)
    win.title("Paramètres du Presse-Papiers")
    win.configure(bg="white")

    win.p1=PI(master = win,file = chemin+"\\color.png")
    win.p2=PI(master = win,file = chemin+"\\threshold.png")

    file = open(chemin+"\\Params.txt","r")
    p = file.readlines()
    file.close()
    parameters=[int(p[0]),int(p[1]),int(p[2]),p[3][:-1],float(p[4]),int(p[5]),int(p[6])]

    frame0 = Frame(win,bg="white")
    frame0.grid(row=0,column=0,columnspan=3)
    col=0
    for arg in list(zip(["Sons","Animations visuelles","Auto-suppression"],[parameters[0],parameters[1],parameters[6]])):
        c=Checkbutton(frame0, text = arg[0],bg="white")
        c.bind("<ButtonRelease-1>", set_parameters)
        c.grid(row=0,column=col,sticky='w',padx=50,pady=10)
        if arg[1]:
            c.select()
        else:
            c.deselect()
        if arg[0] == "Auto-suppression":
            #c.configure(state='disable')
            #c.deselect()
            tooltip.register(c, "Supprime automatique le code tapé suite à un Ctrl + V.")
        col+=1

    frame02 = Frame(win,bg="white")
    frame02.grid(row=1,column=0,columnspan=3)
    thrs = Label(frame02,text="Seuillage",bg="white")
    tooltip.register(thrs, "Segmentation d'une image par sélection de couleurs. (Conseillé : 0.80)")
    thrs.grid(row=1,column=0)
    sp1 = Scale(frame02, from_=0.5, to=1.0, resolution=0.01, orient = HORIZONTAL, command=get_threshold,bg="white",highlightthickness=0,length=200)
    sp1.grid(row=1,column=1, padx=15)
    sp1.set(parameters[4])
    sp1.bind("<MouseWheel>",onMouseWheel1)
    tooltip.register(sp1, "Segmentation d'une image par sélection de couleurs. (Conseillé : 0.80)")

    min_m = Label(frame02,text="Minimum matchs   ",bg="white")
    tooltip.register(min_m, "Le nombre minimal de matchs pour le photomerging.")
    min_m.grid(row=1,column=2)
    sp2 = Scale(frame02, from_=1, to=10, resolution=1, orient = HORIZONTAL, command=get_min_match,bg="white",highlightthickness=0,length=200)    
    sp2.grid(row=1,column=3,pady=15)
    sp2.set(parameters[5])
    sp2.bind("<MouseWheel>",onMouseWheel2)
    tooltip.register(sp2, "Le nombre minimal de matchs pour le photomerging.")

    frame1 = Frame(win,bg="white")
    frame1.grid(row=2,column=0,columnspan=3,pady=10)

    frame1b = Frame(frame1,bd=2,relief=RAISED)
    frame1b.grid(row=0,column=0,padx=50)
    button2 = Button(frame1b, image=win.p1, command = choose_color_v, bd=0)
    button2.pack(side=LEFT)
    l2 =Label(frame1b,text="  Couleur Ctrl+V  ",fg=parameters[3])
    l2.pack(side=RIGHT)
    l2.bind("<ButtonRelease-1>",choose_color_v)
    frame1b.bind("<ButtonRelease-1>",choose_color_v)
    
    frame1c = Frame(frame1,bd=2,relief=RAISED)
    frame1c.grid(row=0,column=1,padx=50)
    button3 = Button(frame1c, image=win.p2, command = lch_reeval, bd=0)
    button3.pack(side=LEFT)
    l3 =Label(frame1c,text=" Réanalyser PhotoMerging ", fg='#f511fb')
    l3.pack(side=RIGHT)
    l3.bind("<ButtonRelease-1>", lch_reeval)
    frame1c.bind("<ButtonRelease-1>", lch_reeval)
    

    label_ft = Label(win, text = "Font Size : ",bg="white")
    label_ft.grid(row=3,column=0,sticky='w',pady=10)
    label_ft.grid_propagate(0)

    s = Scale(win, from_ = 8, to = 84, orient = HORIZONTAL,showvalue=False,length=550,bg="white")
    s.bind("<Motion>", set_fontsize)
    s.set(parameters[2])
    s.grid(row=3,column=1,sticky='w')
    s.grid_propagate(0)

    ft_size_label = Label(win, text = str((3-len(str(s.get())))*"0"+str(s.get())),bg="white")
    ft_size_label.grid(row=3,column=2,sticky='w')
    ft_size_label.grid_propagate(0)

    frame2 = Frame(win,bg="white")
    frame2.grid(row=4,column=0,columnspan=3)
    frame2.grid_propagate(0)
    win.columnconfigure(1, weight=1)

    ex_label2 = Label(frame2, text = "Coller", font = "fixedsys "+str(parameters[2])+" bold", fg=parameters[3],bg="white")
    ex_label2.pack()
    win.withdraw()
    win.mainloop()
    
def onMouseWheel1(event):
    if event.delta == 120:
        sp1.set(sp1.get()+0.01)
    elif event.delta == -120:
        sp1.set(sp1.get()-0.01)
    get_threshold()

def onMouseWheel2(event):
    if event.delta == 120:
        sp2.set(sp2.get()+1)
    elif event.delta == -120:
        sp2.set(sp2.get()-1)
    get_min_match()

def onWheel(event):
    cs.yview_scroll(int(-1*(event.delta/120)), "units")

def copy_paste_historique():
    global his, cs, interior
    his = Tk()
    his.overrideredirect(True)
    his.title("Historique Copy-Paste")
    his.configure(bg="white")
    size = GetMonitorInfo(MonitorFromPoint((0,0))).get('Work')
    height = size[3]-size[1]
    width = size[2]-300
    his.geometry("{}x{}+{}+{}".format(300, height, width, size[1]))

    fr1 = Frame(his,bg="#302f4f")
    fr1.pack(fill=X)
    
    t = Label(fr1,text="Historique Ctrl+C", fg="white", bg="#302f4f")
    t.pack(side=TOP, fill=X)

    vscrollbar = Scrollbar(his, orient=VERTICAL)
    vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)

    cs = Canvas(his, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set,height=height-t.winfo_height(),width=300)
    cs.pack(side=LEFT, fill=BOTH, expand=TRUE)
    
    vscrollbar.config(command=cs.yview)
    
    # reset the view
    cs.xview_moveto(0)
    cs.yview_moveto(0)
    
    # create a frame inside the canvas which will be scrolled with it
    interior = Frame(cs)
    interior_id = cs.create_window(0, 0, window=interior, anchor=NW)
    cs.config(scrollregion="0 0 %s %s" % (300,height-t.winfo_height()))

    his.bind("<MouseWheel>",onWheel)
    his.withdraw()
    his.mainloop()

def get_parameters():
    global parameters, fontsize, ft_size_label, s, ex_label2, win, photo1, start_audio
    try:
        reeval.ROOT.withdraw()
    except:
        pass
    win.deiconify()
    win.attributes("-topmost", True)
    his.deiconify()
    his.attributes("-topmost", True)
    his.lift()
    if not start_audio:
        start_audio=int(time.time())

    threading.Thread(target=playsound,args=("Eric Skiff - Arpanauts",)).start()
    # Gets both half the screen width/height and window width/height
    size = GetMonitorInfo(MonitorFromPoint((0,0))).get('Work')
    height = size[3]-size[1]
    width = size[2]-size[0]
    positionRight = int(width/2 - 650/2)
    positionDown = int(height/2 - 640/2)
    win.geometry("+{}+{}".format(positionRight, positionDown))

def set_fontsize(event):
    global parameters
    lbl.configure(font="fixedsys "+str(s.get())+" bold")
    parameters[2]=s.get()
    ft_size_label.configure(text=str((3-len(str(parameters[2])))*"0"+str(parameters[2])))
    ex_label2.configure(font="fixedsys "+str(s.get())+" bold")
    write_parameters()

def copy_fx():
    global words, number_c
    number_c.append(str(int(number_c[-1])+1))
    try:
        number_c.remove('-1')
    except:
        pass
    time.sleep(0.5)
    word = clipboard.paste()

    words.append(word)

    

    update_historique()
    return False

def paste_fx(by_clic=False):
    global tip_time
    tip_time=time.time()+time.time()
    listener.stop()
    if number_v in number_c:
        print(number_c)
        nv=number_v #permet d'éviter la remise à None de number_v sur un autre thread
        threading.Thread(target=playsound,args=("paste",)).start()
        threading.Thread(target=pop_up,args=("Ctrl + V",str(nv),0.068,0.45,)).start()
        time.sleep(1)
        if parameters[6]:
            if not by_clic:
                w=""
                for l in str(number_v):
                    w+='backspace,'
                KEYBOARD.press_and_release(w[:-1])
            #try:
            #    word = clipboard.paste()
            #except:
            #    word=""
            #try:
                #word = word.encode('utf8', 'ignore')
                #word = word.decode('utf8', 'ignore')
                #if not by_clic:
                #    word=word+nv                
                #COUNT = len(word)-word.count('\n')
                #w=""
                #for l in range(0,COUNT):
                #    w+='backspace,'
                #KEYBOARD.press_and_release(w[:-1])
            #except:
                #pass
        word = words[number_c.index(nv)]
        clipboard.copy(word)
        KEYBOARD.press_and_release('ctrl+v')
             
        his.withdraw()
        
        return False
    
    else:
        listener.stop()
        return False

def test_tip_numpad():
    while 1:
        if time.time()-tip_time>1.5 :
            threading.Thread(target=paste_fx).start()
            time.sleep(5)
        time.sleep(0.10)

def on_Release(key):
    global number_v, passed, listener, tip_time
    try:
        exit = key.char
        
        if str(key) in num_pad :
            number_v+=str(num_pad.index(str(key)))
            tip_time=time.time()

        elif exit.lower() != 'v' and exit in string.printable :
            listener.stop()
            his.withdraw()
            return False
    except:
        
        try:
            if key.name == "ctrl_l" or key.name =="shift":
                if passed<1:
                    passed+=0.5    
                else:
                    threading.Thread(target=paste_fx).start()
            else:
                listener.stop()
                his.withdraw()
                return False

        except:
            his.withdraw()
            print('bug on_release')
            return False

def ctrl_c():
    threading.Thread(target=copy_fx).start()

def ctrl_v():
    global passed, number_v
    number_v = ""
    passed = 0
    his.deiconify()
    his.lift()
    his.attributes('-topmost', True)
    try:
        listener.stop()
    except:
        pass

    threading.Thread(target=launch_listener).start()

#@profile
def screenshot(first):
    global screens, pcd_screens
    threading.Thread(target=play_sound,args=(200,200,)).start()
    im = ImageGrab.grab()
    tns = str(time.time_ns())
    pathname = chemin+"\\Screenshots\\"+tns+'xXx.jpg'
    im.save(pathname)
    if first or len(pcd_screens)==0:
        pcd_screens = [tns,pathname,im.size,True]
        return

    try:
        if((int(tns)-int(screens[-1][0]))/10**9) > 60:
            MessageBox = ctypes.windll.user32.MessageBoxW
            question = MessageBox(None, 'Temps entre deux screens > 60 secondes !\nVoulez vous continuer le photomerging ?', 'PHOTOMERGING',  win32con.MB_YESNO)
            if question != win32con.IDYES:
                screens= []
                pcd_screens= []
                return
    except:
        if((int(tns)-int(pcd_screens[0]))/10**9) > 60:
            MessageBox = ctypes.windll.user32.MessageBoxW
            question = MessageBox(None, 'Temps entre deux screens > 60 secondes !\nVoulez vous continuer le photomerging ?', 'PHOTOMERGING',  win32con.MB_YESNO)
            if question != win32con.IDYES:
                screens= []
                pcd_screens= []
                return
 
    screens.append([tns,pathname,im.size])

    threading.Thread(target=th_screen_match,args=(im,pathname,tns,)).start()

def th_screen_match(im,pathname,tns):
    global running
    while running:
        time.sleep(0.1)
    running += 1
    #print("HERE TH SCREEN MATCH")
    screen_match(im,pathname,tns)

def screen_match(im,pathname,tns):
    global pcd_screens, running, min_coords
    if running > 1:
        print("BUG DE SUPPERPOSITION DE THREAD")
        return
    x, y = im.size
    path_pcd_img = pcd_screens[1]
    pcd_im = cv2.imread(path_pcd_img)
    pcd_im_grey = cv2.imread(path_pcd_img,0) #grey
    img = cv2.imread(pathname,0) #grey

    ord_crops_img_pcd = [[pcd_im, pcd_im_grey, (0,0)]]
    if running > 1:
        print("BUG DE SUPPERPOSITION DE THREAD")
        return
    if pcd_im.shape[1] > GetSystemMetrics(0) or pcd_im.shape[0] > GetSystemMetrics(1):

        crops_imgs_pcd = []
        ord_crops_img_pcd = []
        dx = int(GetSystemMetrics(0)/3)
        dy = int(GetSystemMetrics(1)/3)
        X, Y = pcd_im.shape[1], pcd_im.shape[0]

        starts_x=[x for x in range(0,X,dx)]
        ends_x=[x for x in range(dx,X+dx,dx)]
        starts_y=[y for y in range(0,Y,dy)]
        ends_y=[y for y in range(dy,Y+dy,dy)]

        for id2, sy in enumerate(starts_y):
            for id1, sx in enumerate(starts_x):
                pcd = pcd_im[sy:ends_y[id2],sx:ends_x[id1]]
                pcd_grey = pcd_im_grey[sy:ends_y[id2],sx:ends_x[id1]]
                crops_imgs_pcd.append([pcd, pcd_grey, (sx,sy)])

        array=[] 
        row=[]
        for c in crops_imgs_pcd:
            row.append(c)
            if len(row) == math.ceil(X/dx):
                array.append(row)
                row = []

        lT,lR,lB,lL = Methodic(array, len(crops_imgs_pcd))


        for id, liste in enumerate([lT,lR,lB,lL]):
            for crop in liste:
                if (cv2.countNonZero(crop[1]) * 100) / (crop[1].shape[1] * crop[1].shape[0]) > 45 \
                and crop[1].shape[1] > (3 * (GetSystemMetrics(0) / 15)) \
                and crop[1].shape[0] > (3 * (GetSystemMetrics(1) / 15)) \
                and crop[2][0] > min_coords[0] and crop[2][0] < min_coords[0]+x \
                and crop[2][1] > min_coords[1] and crop[2][1] < min_coords[1]+y :
                    ord_crops_img_pcd.append(crop)

        without_predict_crops = []
        for id, liste in enumerate([lT,lR,lB,lL]):
            for crop in liste:
                if (cv2.countNonZero(crop[1]) * 100) / (crop[1].shape[1] * crop[1].shape[0]) > 45 \
                and crop[1].shape[1] > (3 * (GetSystemMetrics(0) / 15)) \
                and crop[1].shape[0] > (3 * (GetSystemMetrics(1) / 15)) \
                and not (crop[2][0] > min_coords[0] and crop[2][0] < min_coords[0]+x) \
                and not (crop[2][1] > min_coords[1] and crop[2][1] < min_coords[1]+y ):
                    without_predict_crops.append(crop)

        ord_crops_img_pcd+=without_predict_crops
    if running > 1:
        print("BUG DE SUPPERPOSITION DE THREAD")
        return
    nb_of_test = 0
    while nb_of_test < 3:
        for id, obj in enumerate(ord_crops_img_pcd):        
            divisors = [10,15,30]
            dx = int(x/divisors[nb_of_test])
            dy = int(y/divisors[nb_of_test])
    
            starts_x=[x for x in range(0,x,dx)]
            ends_x=[x for x in range(dx,x+dx,dx)]
            starts_y=[y for y in range(0,y,dy)]
            ends_y=[y for y in range(dy,y+dy,dy)]
    
            liste=[] #Doit contenir toutes les images crops im
    
            for id2, sy in enumerate(starts_y):
                for id1, sx in enumerate(starts_x):
                    crop = img[sy:ends_y[id2],sx:ends_x[id1]]
                    liste.append([crop,(sx,sy)])
    
            array=[] #Array
            row=[]
            for c in liste:
                row.append(c)
                if len(row) == divisors[nb_of_test]:
                    array.append(row)
                    row = []
    
            reversed_liste = Spiral(len(array), len(array[0]), array, len(liste),-1)
            lT,lR,lB,lL = Methodic(array, len(liste))
            t0=time.time()
            if running > 1:
                print("BUG DE SUPPERPOSITION DE THREAD")
                return
            c1,c2,rect_x,rect_y = thread_match(obj[0], obj[1],[lT,lR,lB,lL],reversed_liste, array, nb_of_test=nb_of_test, threshold=float(parameters[4]), min_match=int(parameters[5]), add_coords=obj[2])
            t1=time.time()
            if c1 != None:
                to_print="copy_paste Timer : "+str(t1-t0)+" secs to found : "+str((c1,c2))
                print(to_print)
                break
            else:
                to_print="copy_paste Timer : "+str(t1-t0)+" secs -NOT FOUND - : "+str((c1,c2))
                print(to_print)
 
        if c1 != None :
            break
        nb_of_test+=1

    if c1 == None:
        running=False
        return

    min_coords = c2


    img_pcd_size = pcd_screens[2]
    size_x = max(img_pcd_size[0]+c1[0],x+c2[0])
    size_y = max(img_pcd_size[1]+c1[1],y+c2[1])
    
    new = Image.new("RGB", (size_x, size_y), "Black")
    
    img1 = Image.open(path_pcd_img)         
    new.paste(img1, c1)
    img2 = Image.open(pathname)         
    new.paste(img2, c2)
    
    pcd_name = os.path.basename(path_pcd_img)
    pcd_tns = pcd_name.strip('xXxresult.jpg')
    
    result_path = chemin+"\\Screenshots\\"+pcd_tns+"xXx"+tns+"xXxresult.jpg"
    new.save(result_path)
    print("RESULT SAVED",(int(time.time_ns())-int(tns))/10**9)
    if not pcd_screens[3]:
        os.remove(pcd_screens[1])
    pcd_screens = [tns, result_path, new.size,False]
    
    threading.Thread(target=play_sound,args=(750,200,)).start()
    running=False
    return

def play_sound(freq,dur):
    winsound.Beep(freq,dur)

def press_ss(key):
    global shift_pressed, option_pressed, screens, pcd_screens
    try:
        if key.name == "shift":
            shift_pressed=True
        elif key.name == 'print_screen' and not shift_pressed and not option_pressed :
            if len(screens) > 0:
                if int((int(time.time_ns())-int(screens[-1][0]))/10**9) < 30:
                    MessageBox = ctypes.windll.user32.MessageBoxW
                    question = MessageBox(None, 'Un photomerging était récemment en cours, voulez-vous en réaliser un nouveau ?', 'Nouveau photomerging ?',  win32con.MB_YESNO)
                    if question != win32con.IDYES:
                        screens = []
                        pcd_screens = []
                        screenshot(False)
                        return
                else:
                    pcd_screens = []
                    screens = []
            screenshot(True)
        elif key.name == 'print_screen' and not option_pressed :
            screenshot(False)
    except:
        pass

def paste_by_clic(event):
    global number_v
    number_v = event.widget.num
    his.withdraw()
    threading.Thread(target=paste_fx,args=(True,)).start()

def update_historique():
    for ch in interior.winfo_children():
        ch.destroy()
    his.update()
    length = 0
    for num,txt in list(zip(number_c,words)):
        if num:
            #pass
            fra = Frame(interior, bd=0, highlightthickness=0,bg="#446d99",height=200,width=280)
            fra.pack_propagate(0)
            fra.pack(fill=BOTH, side=TOP, expand=TRUE)
            fra.num = num
            fra.bind("<ButtonRelease-1>", paste_by_clic)

            lbl_num = Label(fra,text=str(num), bg="#446d99", fg="white",height=1)
            lbl_num.pack_propagate(0)
            lbl_num.pack(fill=X, side=TOP)
            lbl_num.num = num
            lbl_num.bind("<ButtonRelease-1>", paste_by_clic)
            
            ca = Canvas(fra, bg="white",height=200,width=280)
            ca.pack_propagate(0)
            ca.pack(fill=BOTH, side=TOP, expand=False,padx=5,pady=5)
            ca.num = num
            ca.bind("<ButtonRelease-1>", paste_by_clic)

            vscrollbar = Scrollbar(ca, orient=VERTICAL)
            vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)

            hscrollbar = Scrollbar(ca, orient=HORIZONTAL)
            hscrollbar.pack(fill=X, side=BOTTOM, expand=TRUE)

            inside_ca = Canvas(ca, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, height=200,width=280,bg='white')
            inside_ca.pack(side=LEFT, fill=BOTH, expand=TRUE)
            inside_ca.num = num
            inside_ca.bind("<ButtonRelease-1>", paste_by_clic)

            vscrollbar.config(command=inside_ca.yview)
            hscrollbar.config(command=inside_ca.xview)

            inside_ca.xview_moveto(0)
            inside_ca.yview_moveto(0)

            inter = Frame(inside_ca)
            inter_id = inside_ca.create_window(0, 0, window=inter, anchor=NW)
            inter.num = num
            inter.bind("<ButtonRelease-1>", paste_by_clic)

            txt_lbl = Label(inter, text=txt, bg='white', justify='left')
            txt_lbl.pack()
            txt_lbl.num = num
            txt_lbl.bind("<ButtonRelease-1>", paste_by_clic)

            his.update()

            LENGTH = txt_lbl.winfo_height()
            WIDTH = txt_lbl.winfo_width()

            inside_ca.config(scrollregion="0 0 %s %s" % (WIDTH,LENGTH))
            
            length+=fra.winfo_height()

    size = GetMonitorInfo(MonitorFromPoint((0,0))).get('Work')
    height = size[3]-size[1]
    width = size[2]-300
    his.geometry("{}x{}+{}+{}".format(300, height, width, size[1]))
    length = max(height,length)
    cs.config(scrollregion="0 0 %s %s" % (300,length))
    cs.xview_moveto(0)
    cs.yview_moveto(0)
    his.update()

def press_option(key):
    global option_pressed, shift_pressed
    try:
        exit = key.char
        if str(key) == '<222>' and shift_pressed:
            #print('shift+² pressé')
            option_pressed = True
            threading.Thread(target=get_parameters).start()

    except:
        try:
            if key.name == "shift":
                shift_pressed = True
        except:
            option_pressed = False
            shift_pressed = False

def release_option(key):
    global option_pressed, shift_pressed
    try:
        if key.char == '²':
            option_pressed = False
            shift_pressed = False
    except:
        try:
            if key.name == "shift":
                print('shift relaché')
                option_pressed = False
                shift_pressed = False
        except:
            option_pressed = False
            shift_pressed = False

def release_ss(key):
    global shift_pressed, option_pressed
    try:
        if key.name == "shift":
            shift_pressed=False
    except:
        try:
            if key.char == '²':
                option_pressed=False
        except:
            pass

def thread_options():
    with keyboard.Listener(
        on_press=press_option,
        on_release=release_option) as lst:
        lst.join()

def thread_print_screen():
    global ecouteur
    with keyboard.Listener(
        on_press=press_ss,
        on_release=release_ss) as ecouteur:
        ecouteur.join()

threading.Thread(target=root_tk).start()
threading.Thread(target=options).start()
threading.Thread(target=copy_paste_historique).start()
threading.Thread(target=thread_print_screen).start()
threading.Thread(target=thread_options).start()
threading.Thread(target=test_tip_numpad).start()

with keyboard.GlobalHotKeys({
        '<ctrl>+c': ctrl_c,
        '<ctrl>+<shift>+v': ctrl_v,
        }) as h:
    h.join()

'''
#def near_of(coords,width,height):
#    top = (int(width/2), 0)
#    right = (width, int(height/2))
#    bottom = (int(width/2), height)
#    left = (0, int(height/2))
#
#    dist_to_top = [math.sqrt( ((coords[0]-top[0])**2)+((coords[1]-top[1])**2) ),0]
#    dist_to_right = [math.sqrt( ((coords[0]-right[0])**2)+((coords[1]-right[1])**2) ),1]
#    dist_to_bottom = [math.sqrt( ((coords[0]-bottom[0])**2)+((coords[1]-bottom[1])**2) ),2]
#    dist_to_left = [math.sqrt( ((coords[0]-left[0])**2)+((coords[1]-left[1])**2) ),3]
#
#    return sorted([dist_to_top, dist_to_bottom, dist_to_right, dist_to_left])'''