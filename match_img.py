import cv2, time, os, random, threading
import numpy as np
from run_array import Spiral

# All the 6 methods for comparison
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
colors = [(0,0,255),(0,255,0),(255,0,0),(255,0,255),(255,255,0)] #rouge, Vert, Bleu, Rose, Jaune
chemin = os.path.expanduser('~\Copy_Paste\\Screenshots\\grid.jpg')

def thread_match(pcd_im, img1_gray, listes, reversed_liste, array, nb_of_test=1):
	global COORDS_1, COORDS_2, C1, C2, copy
	COORDS_1, COORDS_2 , ths = [], [], [] #[x,y] de l'image 1, 2 et liste des threads des listes Methodic
	C1, C2 = None, None
	copy = pcd_im.copy()
	if nb_of_test == 1:
		threading.Thread(target=find_match,args=(img1_gray, reversed_liste, [], 5, True)).start() #Thread de recherche par reverse_spiral

	for l in listes:
		th = threading.Thread(target=find_match,args=(img1_gray, l, array, nb_of_test))
		th.start()
		ths.append(th)

	time.sleep(0.1)
	while C1 == None:
		alive = False
		for th in ths:
			if th.isAlive():
				alive=True
				continue
		if not alive:
			break
	
	return C1, C2

def test(pt, coords):
	global COORDS_1, COORDS_2, C1, C2
	COORDS_1.append((max(0,coords[0]-pt[0]),max(0,coords[1]-pt[1])))
	COORDS_2.append((max(0,COORDS_1[-1][0]-(coords[0]-pt[0])),max(0,COORDS_1[-1][1]-(coords[1]-pt[1]))))
	try:
		cs_1=COORDS_1.copy()
		cs_2=COORDS_2.copy()
		for c1 in cs_1:
			if cs_1.count(c1)>1: 
				indices = [i for i, x in enumerate(cs_1) if x == c1]
				new_coords_2 = [c for c in [cs_2[id] for id in indices]]
				for c2 in new_coords_2:
					if new_coords_2.count(c2)>1:
						if (c1,c2) != ((0,0),(0,0)):
							C1=c1
							C2=c2
							return
	except:	
		pass

def find_match(img1_gray, crops, array, nb_of_test=1, spiral=False):
	global COORDS_1, COORDS_2, C1, C2, copy
	w2, h2 = crops[0][0].shape[::-1]
	#for img in random.sample(crops,len(crops)):
	t_start = time.time()
	for img in crops:
		if C1 or (spiral and (time.time()-t_start) > 2.5):
			return
		img2=img[0]
		res = cv2.matchTemplate(img1_gray,img2,cv2.TM_CCOEFF_NORMED)
		threshold = 0.95
		loc = np.where(res >= threshold)
		try:
			pt = list(zip(*loc[::-1]))[0]
			#cv2.rectangle(copy, pt, (pt[0] + w2, pt[1] + h2), colors[nb_of_test-1], 1*nb_of_test)
			#cv2.imwrite(chemin,copy)
			coords = img[1] #coordonnées du crop
			test(pt, coords)
			if C1:
				#print("COORDS FOUND DUE TO PRIMARY SEARCHING")
				return
			if not spiral:
				for r, row in enumerate(array):
					try:
						c = row.index(img)
						new_array = array[max(0,r-1)][max(0,c-1):min(c+2,len(row)-1)]+\
									[array[r][max(0,c-1)],array[r][min(c+1,len(row)-1)]]+\
									array[min(r+1,len(array)-1)][max(0,c-1):min(c+2,len(row)-1)]
						new_array=[x for x in new_array if new_array.count(x)==1]
						break
					except:
						pass
				for img in new_array:
					img2=img[0]
					res = cv2.matchTemplate(img1_gray,img2,cv2.TM_CCOEFF_NORMED)
					threshold = 0.95
					loc = np.where(res >= threshold)
					try:
						pt = list(zip(*loc[::-1]))[0]
						#cv2.rectangle(copy, pt, (pt[0] + w2, pt[1] + h2), colors[3], 3)
						#cv2.imwrite(chemin,copy)
						coords = img[1]
						test(pt, coords)
						if C1:
							#print("COORDS FOUND DUE TO ARROUND SEARCHING")
							return
					except:
						pass
		except:
			pass
	return None, None
