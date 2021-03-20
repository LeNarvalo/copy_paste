from tkinter.filedialog import askopenfilename
import time, os, ctypes, win32con, cv2, winsound, threading, math
from PIL import Image as IMAGE
from PIL import ImageTk as IMAGETK
from match_img import thread_match, ths, annuler_match
from run_array import Spiral, Methodic
from tkinter import *
from tkinter.ttk import Progressbar
from win32api import GetSystemMetrics

chemin = os.path.expanduser('~\Copy_Paste\\Screenshots')
screens = []
pcd_screens = []
CONTINUER = "unknown"
ANNULATION = False
FINISHED = False
accuracy = 0.80
minimum_match = 2
PATHNAME = ""
min_coords = (0,0)
class ROOT:
    None

def widget(threshold, min_match):
    global accuracy, minimum_match
    accuracy = threshold
    minimum_match = min_match
    if 'bar' not in globals():
        threading.Thread(target=create_ROOT).start()
    else:
        LBL.configure(text="Choississez une image à réassembler.")
        timer.configure(text=" ")
        com.configure(state=DISABLED)
        ope.configure(state=NORMAL)
        acc.set(int(accuracy*100))
        min_m.set(int(minimum_match))
        ROOT.deiconify()
        ROOT.attributes("-topmost", 1)
        ROOT.lift()

def open_file():
    global PATHNAME
    PATHNAME = askopenfilename( title = "Sélectionnez une image à réanalyser ...", \
                                initialdir = chemin, \
                                filetypes = [("Images","result.jpg")])
    com.configure(state=NORMAL)
    nb_of_imgs = len(os.path.basename(PATHNAME).split('xXx')[:-1])
    if 1 > nb_of_imgs < 2:
        timer.configure(text="Image non compatible")
        time.sleep(0.5)
        init()
        return

def commencer():
    global TIMER, CONTINUER
    CONTINUER = "unknown"
    if PATHNAME == "":
        timer.configure(text="Choisissez une image d'abord !")
        return
    ope.configure(state=DISABLED)
    com.configure(state=DISABLED)
    TIMER = time.time()
    threading.Thread(target=update_timer).start()
    threading.Thread(target=thread_start).start()
    ann.configure(state=NORMAL)
    bar.start(15)

def thread_start():
    global PATHNAME, nb_of_imgs 
    try:
        nb_of_imgs = len(os.path.basename(PATHNAME).split('xXx')[:-1])
        for i, tns in enumerate(os.path.basename(PATHNAME).split('xXx')[:-1]):
            if i == 0:
                print('0',tns)
                screenshot(True,tns, i)
            else:
                print('1',tns)
                if screenshot(False,tns, i):
                    time.sleep(0.2)
                    timer.configure(text="Résultat final enregistré",fg="green")
        time.sleep(2)
        init()

    except:
        #ROOT.withdraw()
        pass

def windows(message,title,type):
    global CONTINUER, TIMER
    time.sleep(1)
    MessageBox = ctypes.windll.user32.MessageBoxW
    question = MessageBox(None, message, title,  type)
    if question == win32con.IDNO and title == 'PHOTOMERGING':
        CONTINUER = False
        LBL.configure(text="Nouveau niveau d'analyse !")
        timer.configure(text="0 sec", fg="red")
        ROOT.update()
        time.sleep(2)
        TIMER = time.time()
        raat.withdraw()

    elif question == win32con.IDCANCEL and title == 'PHOTOMERGING':
        raat.withdraw()
        annulation()

    elif title == 'PHOTOMERGING':
        CONTINUER=True
        raat.withdraw()

def create_raat(NEW):
    global raat, canvas, cid
    raat = Toplevel(ROOT)
    raat.resizable(0,0)
    raat.protocol("WM_DELETE_WINDOW", on_closing2)
    width = int(ROOT.winfo_screenwidth() / max(1,NEW.size[1]/ROOT.winfo_screenheight()))
    height = int(ROOT.winfo_screenheight() / max(1,NEW.size[0]/ROOT.winfo_screenwidth()))
    NEW.thumbnail((width , height))
    canvas = Canvas(raat, width = NEW.size[0], height = NEW.size[1])  
    canvas.pack()  
    img = IMAGETK.PhotoImage(NEW,master=raat)
    cid = canvas.create_image(20, 20, anchor=NW, image=img)
    raat.update()
    windowWidth = raat.winfo_reqwidth()
    windowHeight = raat.winfo_reqheight()
    positionRight = int((ROOT.winfo_screenwidth()/2 - windowWidth/2))
    positionDown = int((ROOT.winfo_screenheight()/2 - windowHeight/2))
    raat.geometry("{}x{}+{}+{}".format(width, height, positionRight, positionDown))

def on_closing2():#remplacer close cross par withdraw
    raat.withdraw()

def show_reeval(new):
    NEW = new.copy()
    width = int(ROOT.winfo_screenwidth() / max(1,NEW.size[1]/ROOT.winfo_screenheight()))
    height = int(ROOT.winfo_screenheight() / max(1,NEW.size[0]/ROOT.winfo_screenwidth()))
    NEW.thumbnail((width, height))

    if 'raat' not in globals():
        threading.Thread(target=create_raat,args=(NEW,)).start()
    else:
        raat.deiconify()
        img = IMAGETK.PhotoImage(NEW,master=raat)
        canvas.itemconfigure(cid, image = img)
        canvas.image = img
        raat.update()
        windowWidth = raat.winfo_reqwidth()
        windowHeight = raat.winfo_reqheight()
        positionRight = int((ROOT.winfo_screenwidth()/2 - windowWidth/2))
        positionDown = int((ROOT.winfo_screenheight()/2 - windowHeight/2))
        raat.geometry("{}x{}+{}+{}".format(width, height, positionRight, positionDown))
        raat.update()
    threading.Thread(target=windows, args = ("L'assemblage vous convient-il ?", 'PHOTOMERGING', win32con.MB_YESNOCANCEL | win32con.MB_SYSTEMMODAL, )).start()

def screenshot(first,tns,i):
    global screens, pcd_screens, CONTINUER, TIMER, FINISHED, min_coords
    pathname = chemin+"\\"+tns+'xXx.jpg'
    im = IMAGE.open(pathname)
    print("##################################")
    if first or len(pcd_screens)==0:
        pcd_screens = [tns,pathname,im.size,True]
        return False

    screens.append([tns,pathname,im.size])

    x, y = im.size
    path_pcd_img = pcd_screens[1]
    pcd_im = cv2.imread(path_pcd_img)
    pcd_im_grey = cv2.imread(path_pcd_img,0) #grey
    img = cv2.imread(pathname,0) #grey

    print("TEST")
    ord_crops_img_pcd = [[pcd_im, pcd_im_grey, (0,0)]]

    if pcd_im.shape[1] > GetSystemMetrics(0) or pcd_im.shape[0] > GetSystemMetrics(1):
        print('pcd img to big')
        crops_imgs_pcd = []
        dx = int(GetSystemMetrics(0)/3)
        dy = int(GetSystemMetrics(1)/3)
        X, Y = pcd_im.shape[1], pcd_im.shape[0]
        print(dx, dy)
        starts_x=[x for x in range(0,X,dx)]
        ends_x=[x for x in range(dx,X+dx,dx)]
        starts_y=[y for y in range(0,Y,dy)]
        ends_y=[y for y in range(dy,Y+dy,dy)]

        for id2, sy in enumerate(starts_y):
            for id1, sx in enumerate(starts_x):
                pcd = pcd_im[sy:ends_y[id2],sx:ends_x[id1]]
                pcd_grey = pcd_im_grey[sy:ends_y[id2],sx:ends_x[id1]]
                crops_imgs_pcd.append([pcd, pcd_grey, (sx,sy)])
                #print(id2,id1,cv2.countNonZero(pcd_grey))# compte le nombre de pixel non noir
                #print('sx,sy',(sx,sy))

        array=[] #Array
        row=[]
        for c in crops_imgs_pcd:
            row.append(c)
            if len(row) == math.ceil(X/dx):
                array.append(row)
                row = []
        #print('row',len(array),'column',len(array[0]))
        lT,lR,lB,lL = Methodic(array, len(crops_imgs_pcd))
        #print(len(lT),len(lR),len(lB),len(lL))

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
    print('ici 219')
    nb_of_test = 0
    while nb_of_test < 3:
        if ANNULATION:
            return False
        LBL.configure(text="Réassamblage en cours ("+str(i)+"/"+str(nb_of_imgs)+")\n NIVEAU "+str(nb_of_test+1)) #bug qd annuler
        for id, obj in enumerate(ord_crops_img_pcd):
            if ANNULATION:
                return False
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

            if ANNULATION:
                return False
    
            reversed_liste = Spiral(len(array), len(array[0]), array, len(liste),-1)
            lT,lR,lB,lL = Methodic(array, len(liste))

            t0=time.time()
            print(id, nb_of_test, "Start :",t0)
            c1,c2,rect_x,rect_y = thread_match(obj[0], obj[1],[lT,lR,lB,lL],reversed_liste, array, nb_of_test=nb_of_test, threshold=float(accuracy), min_match=int(minimum_match), add_coords=obj[2])
            t1=time.time()

            if ANNULATION:
                return False

            if c1 != None:
                to_print="reeval Timer : "+str(t1-t0)+" secs to found : "+str((c1,c2))
                print(to_print)
                break
            else:
                to_print="reeval Timer : "+str(t1-t0)+" secs -NOT FOUND - : "+str((c1,c2))
                print(to_print)

        nb_of_test+=1

        if c1 != None :
            min_coords = c2

            bar.stop()

            img_pcd_size = pcd_screens[2]
            size_x = max(img_pcd_size[0]+c1[0],x+c2[0])
            size_y = max(img_pcd_size[1]+c1[1],y+c2[1])
            
            new = IMAGE.new("RGB", (size_x, size_y), "Black")
            
            img1 = IMAGE.open(path_pcd_img)         
            new.paste(img1, c1)
            img2 = IMAGE.open(pathname)         
            new.paste(img2, c2)
            
            threading.Thread(target=show_reeval,args=(new,)).start()
            #print('Là')
            while CONTINUER == "unknown":
                time.sleep(0.1)
                if ANNULATION:
                    return False
            #print('Là 2')
            if not CONTINUER:
                continue

            pcd_name = os.path.basename(path_pcd_img)
            pcd_tns = pcd_name.strip('xXxresult.jpg')

            result_path = chemin+"\\"+pcd_tns+"xXx"+tns+"xXxresult.jpg"
            new.save(result_path)
            print("RESULT SAVED")
            if not pcd_screens[3]:
                os.remove(pcd_screens[1])
            pcd_screens = [tns, result_path, new.size,False]

            CONTINUER = "unknown"

            TIMER = time.time()
            if i+1 == nb_of_imgs:
                FINISHED = True
                LBL.configure(text="Réassamblage terminé ("+str(i+1)+"/"+str(nb_of_imgs)+")")
                return True
            #time.sleep(2)    
            return False

    if c1 == None:
        print("NOT FOUND")
        threading.Thread(target=windows, args = ("Le logiciel n'a pas réussi à assembler les images !", 'AUCUN RESULTAT', win32con.MB_ICONERROR, )).start()
        return False

'''
def screenshot(first,tns,i):
    global screens, CONTINUER, c1, TIMER
    #print(tns)
    pathname = chemin+'\\'+tns+'xXx.jpg'
    #print(pathname)
    im = IMAGE.open(pathname)
    #print(im.size)
    screens.append([tns,pathname,im.size,False])

    if first :
        return

    x, y = im.size
    nb_of_test = 0
    path_pcd_img = screens[-2][1]
    pcd_im = cv2.imread(path_pcd_img)
    pcd_im_grey = cv2.imread(path_pcd_img,0) #grey
    img = cv2.imread(pathname,0) #grey
    #print(pcd_im)

    while nb_of_test < 3:
        if ANNULATION:
            return
        LBL.configure(text="Réassamblage en cours ("+str(i)+"/"+str(nb_of_imgs)+")\n NIVEAU "+str(nb_of_test+1)) #bug qd annuler
        divisors = [15,30,60]
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
        #print('len(array)',len(array))
        if ANNULATION:
            return
        nb_of_test+=1
        reversed_liste = Spiral(len(array), len(array[0]), array, len(liste),-1)
        lT,lR,lB,lL = Methodic(array, len(liste))
        t0=time.time()
        c1,c2 = thread_match(pcd_im, pcd_im_grey,[lT,lR,lB,lL],reversed_liste, array, nb_of_test, accuracy, min_match)
        t1=time.time()
        
        if ANNULATION:
            return

        if c1 == None:
            continue

        img_pcd_size = screens[-2][2]
        size_x = max(img_pcd_size[0]+c1[0],x+c2[0])
        size_y = max(img_pcd_size[1]+c1[1],y+c2[1])
        
        new = IMAGE.new("RGB", (size_x, size_y), "Black")
    
        img1 = IMAGE.open(path_pcd_img)
        new.paste(img1, c1)
        img2 = IMAGE.open(pathname)
        new.paste(img2, c2)

        bar.stop()
 
        threading.Thread(target=show_reeval,args=(new,)).start()

        while CONTINUER == "unknown":
            time.sleep(0.1)
            if ANNULATION:
                return

        if not CONTINUER:
            continue
            
        
        pcd_name = os.path.basename(path_pcd_img)
        pcd_tns = pcd_name.strip('xXxnew_result.jpg')
    
        result_path = chemin+"\\"+pcd_tns+"xXx"+tns+"xXxnew_result.jpg"
        new.save(result_path)
        print("RESULT SAVED")
        screens.append([tns, result_path, new.size, True])
        CONTINUER = "unknown"
        winsound.Beep(750,200)
        TIMER = time.time()
        if i+1 == nb_of_imgs:
            LBL.configure(text="Réassamblage terminé ("+str(i+1)+"/"+str(nb_of_imgs)+")")
            timer.configure(text="Résultat final enregistré",fg="green")
            screens[-1][3]=False
            delete_temp_img()

        time.sleep(2)
        break'''

def annuler():
    threading.Thread(target=annulation).start()

def annulation():
    global CONTINUER, ANNULATION
    CONTINUER = False
    ANNULATION = True
    annuler_match(True)
    bar.stop()
    ann.configure(state=DISABLED)
    ROOT.update()
    time.sleep(0.2)
    timer.configure(text="Réassamblage annulé\n",fg="red")
    ROOT.update()

def update_timer():
    print('update_timer()')
    while not FINISHED and not ANNULATION :
        time.sleep(0.1)
        timer.configure(text=str(int(time.time()-TIMER))+" sec",fg="red")

def set_accuracy(event):
    global accuracy
    accuracy = acc.get()/100
 
def set_min_match(event):
    global minimum_match
    minimum_match = min_m.get()
 
def on_closing():#remplacer close cross par withdraw
    ROOT.withdraw()
    annulation()

def init():
    global PATHNAME, ANNULATION, screens, pcd_screens, CONTINUER, FINISHED
    time.sleep(0.5)
    CONTINUER = "unknown"
    PATHNAME = ""
    bar.stop()
    ope.configure(state=NORMAL)
    com.configure(state=DISABLED)
    ann.configure(state=DISABLED)
    LBL.configure(text="Choississez une image à réassembler.")
    timer.configure(text="",fg="red")
    ROOT.update()
    ANNULATION = False
    screens = []
    pcd_screens = []
    CONTINUER = True
    #FINISHED = False
    annuler_match(False)

def create_ROOT():
    global ROOT, bar, LBL, ann, timer, com, ope, acc, min_m
    ROOT = Tk()
    ROOT.title("Réénalyser des images")
    ROOT.resizable(0,0)
    ROOT.attributes('-toolwindow', True)
    ROOT.protocol("WM_DELETE_WINDOW", on_closing)
    #ROOT.overrideredirect(True)
    ROOT.geometry("615x250")
    ROOT.attributes("-topmost", 1)
    LBL = Label(ROOT, text="Choississez une image à réassembler.")
    LBL.grid(row=0,column=0,columnspan=3)
    timer = Label(ROOT, text=" ", fg="red")
    timer.grid(row=1,column=0,columnspan=3)
    bar = Progressbar(ROOT, orient='horizontal', mode='indeterminate', value=0)
    bar.grid(row=2, column=0, sticky=W+E,columnspan=3)
    ope = Button(ROOT, overrelief=GROOVE, text ='Ouvrir une image', command = open_file, width=16)
    ope.grid(row=3,column=0, pady=10)
    com = Button(ROOT, overrelief=GROOVE, text ='Commencer', command = commencer, width=16)
    com.configure(state=DISABLED)
    com.grid(row=3,column=1)
    ann = Button(ROOT, overrelief=GROOVE, text ='Annuler', command = annuler, width=16)
    ann.configure(state=DISABLED)
    ann.grid(row=3,column=2)
    frame = Frame(ROOT)
    frame.grid(row=4,columnspan=3)
    acc = Scale(frame, label="Seuillage (%) (Temporaire)", from_ = 50, to = 100, orient = HORIZONTAL,showvalue=True,length=300)
    acc.grid(row=0,column=0)
    acc.bind("<Motion>", set_accuracy)
    acc.set(int(accuracy*100))
    min_m = Scale(frame, label="Minimum matchs (Temporaire)", from_ = 1, to = 10, orient = HORIZONTAL,showvalue=True,length=300)
    min_m.grid(row=0,column=1)
    min_m.bind("<Motion>", set_min_match)
    min_m.set(minimum_match)
    positionRight = int((ROOT.winfo_screenwidth()/2 - 615/2))
    positionDown = int((ROOT.winfo_screenheight()/2 - 250/2))
    ROOT.geometry("+{}+{}".format(positionRight, positionDown))
    #ROOT.withdraw()
    ROOT.lift()
    ROOT.mainloop()


