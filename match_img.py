import cv2, time, os, random, threading
import numpy as np
from run_array import Spiral
#from memory_profiler import profile

# All the 6 methods for comparison
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
colors = [(0,0,255),(0,255,0),(255,0,0),(255,0,255),(255,255,0)] #rouge, Vert, Bleu, Rose, Jaune
chemin = os.path.expanduser('~\Copy_Paste\\Screenshots\\grid.jpg')
ths=[]
ANNULATION = False

def annuler_match(arg):
    global ANNULATION
    ANNULATION = arg


def thread_match(pcd_im, img1_gray, listes, reversed_liste, array, nb_of_test=0, threshold=0.80, min_match=2, add_coords=(0,0)):
    global COORDS_1, COORDS_2, C1, C2, copy, ths
    while 1:
        alive = False
        for th in ths:
            try:
                if th.isAlive():
                    alive=True
                    continue
            except:
                alive=False
                break
        if not alive:
            break

    COORDS_1, COORDS_2 , ths = [], [], [] #[x,y] de l'image 1, 2 et liste des threads des listes Methodic
    C1, C2 = None, None
    copy = pcd_im.copy()
    if nb_of_test == 0:
        threading.Thread(target=find_match,args=(img1_gray, reversed_liste, [], 5, True, threshold, min_match, add_coords)).start() #Thread de recherche par reverse_spiral

    for l in listes:
        th = threading.Thread(target=find_match,args=(img1_gray, l, array, nb_of_test, False, threshold, min_match, add_coords))
        th.start()
        ths.append(th)

    time.sleep(0.1)
    while C1 == None:
        alive = False
        for th in ths:
            if th.isAlive():
                alive=True
                break
        if not alive or C1:
            break
    
    return C1, C2, rect_x, rect_y


def test(pt, coords, min_match, add_coords, img1_gray, w2, h2, nb_of_test):
    global COORDS_1, COORDS_2, C1, C2, rect_x, rect_y
    COORDS_1.append((max(0,coords[0]-(add_coords[0]+pt[0])),max(0,coords[1]-(add_coords[1]+pt[1]))))
    COORDS_2.append((max(0,(add_coords[0]+pt[0])-coords[0]),max(0,(add_coords[1]+pt[1])-coords[1])))
    try:
        cs_1=COORDS_1.copy()
        cs_2=COORDS_2.copy()
        for c1 in cs_1:
            if ANNULATION:
                return
            if cs_1.count(c1)>=min_match: 
                indices = [i for i, x in enumerate(cs_1) if x == c1]
                new_coords_2 = [c for c in [cs_2[id] for id in indices]]
                for c2 in new_coords_2:
                    if ANNULATION:
                        return
                    if new_coords_2.count(c2)>=min_match:
                        if (c1,c2) != ((0,0),(0,0)) and not ANNULATION:
                            C2=c2
                            C1=c1
                            rect_x = pt[0]
                            rect_y = pt[1]
                            #cv2.rectangle(copy, pt, (pt[0] + w2, pt[1] + h2), colors[nb_of_test], 1*(nb_of_test+1))
                            #cv2.imwrite(chemin,copy)
                            return
    except: 
        pass


def find_match(img1_gray, crops, array, nb_of_test, spiral, threshold, min_match, add_coords):
    global copy
    w2, h2 = crops[0][0].shape[::-1]
    t_start = time.time()
    for img in crops:
        if C1 or (spiral and (time.time()-t_start) > 4) or ANNULATION :
            return
        img2=img[0]
        res = cv2.matchTemplate(img1_gray,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(list(zip(*loc[::-1]))):
            pt = list(zip(*loc[::-1]))[0] #coordonnées du crop sur l'image précédente
            coords = img[1] #coordonnées du crop sur le screenshot en cours
            #cv2.rectangle(copy, pt, (pt[0] + w2, pt[1] + h2), colors[nb_of_test-], 1*(nb_of_test+1))
            #cv2.imwrite(chemin,copy)
            test(pt, coords, min_match, add_coords, img1_gray, w2, h2, nb_of_test)
            if C1:
                return
            if not spiral:
                for r, row in enumerate(array):
                    for c, obj in enumerate(row):
                        if obj[1] == coords:
                            new_array = array[max(0,r-1)][max(0,c-1):min(c+2,len(row))]+\
                                        [array[r][max(0,c-1)],array[r][min(c+1,len(row)-1)]]+\
                                        array[min(r+1,len(array)-1)][max(0,c-1):min(c+2,len(row))]
                            break
                NEW_ARRAY=[]
                cur_coords=[]
                for x in new_array:
                    if x[1] not in cur_coords and x[1] != coords:
                        NEW_ARRAY.append(x)
                        cur_coords.append(x[1])
                for img in NEW_ARRAY:
                    if C1 or ANNULATION:
                        return
                    img2=img[0]
                    res = cv2.matchTemplate(img1_gray,img2,cv2.TM_CCOEFF_NORMED)
                    loc = np.where(res >= threshold)
                    try:
                        pt = list(zip(*loc[::-1]))[0]
                        coords = img[1]
                        test(pt, coords, min_match, add_coords, img1_gray, w2, h2, nb_of_test)
                        if C1:
                            return
                    except:
                        pass

    return None, None
