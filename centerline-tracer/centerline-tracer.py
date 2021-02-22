import numpy as np
import random
import cv2

def show(img):
    cv2.imshow("ha", img)
    cv2.waitKey(0)

def filter_neighbors(ns):    
    i = 0
    while i < len(ns):
        j = i + 1
        while j < len(ns):
            if (ns[i][0] == ns[j][0] and abs(ns[i][1] - ns[j][1]) <= 1) or (ns[i][1] == ns[j][1] and abs(ns[i][0] - ns[j][0]) <= 1):
                del ns[j]
                break                                    
            j += 1
        i += 1    

def sort_points_types(pnts, img):
    extremes = []
    connections = []
    simple = []

    for p in pnts:
        x = p[0]
        y = p[1]
        n = []
        if img[y - 1,x] > 0: n.append((y-1, x))
        if img[y - 1,x - 1] > 0: n.append((y-1, x - 1))
        if img[y - 1,x + 1] > 0: n.append((y-1, x + 1))
        if img[y,x - 1] > 0: n.append((y, x - 1))
        if img[y,x + 1] > 0: n.append((y, x + 1))
        if img[y + 1,x] > 0: n.append((y+1, x))
        if img[y + 1,x - 1] > 0: n.append((y+1, x - 1))
        if img[y + 1,x + 1] > 0: n.append((y+1, x + 1))
        filter_neighbors(n)
        if len(n) == 1:
            extremes.append(p)
        elif len(n) == 2:
            simple.append(p)
        elif len(n) > 2:
            connections.append(p)
    return extremes, connections, simple


img_path = "test.png"

img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

_, th = cv2.threshold(img, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
thin = cv2.ximgproc.thinning(th)
use_cv2 = False

if use_cv2:
    no_ccs, labels = cv2.connectedComponents(thin)

    label_pnts_dic = {}

    colored = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    i = 1 # skip label 0 as it corresponds to the backgground points
    sum_of_cc_points = 0 
    while i < no_ccs:
        label_pnts_dic[i] = np.where(labels == i) #where return tuple(list of x cords, list of y cords)
        colored[label_pnts_dic[i]] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        i += 1

    # for label in label_pnts_dic:
    #     for p in range(0,len(label_pnts_dic[label][0])):
    #         cv2.circle(colored, (label_pnts_dic[label][1][p], label_pnts_dic[label][0][p]), 2, 128)
    #         show(colored)
        
else:
    no_ccs, labels = cv2.connectedComponents(thin)
    label_pnts_dic = {}
    # colored = cv2.cvtColor(thin, cv2.COLOR_GRAY2BGR)

    copy = np.zeros(thin.shape, np.uint8)

    i = 1 # skip label 0 as it corresponds to the backgground points
    sum_of_cc_points = 0 
    while i < no_ccs:
        label_pnts_dic[i] = np.where(labels == i) #where return tuple(list of x cords, list of y cords)
        copy[label_pnts_dic[i]] = 255
        i += 1

    pnts = cv2.findNonZero(copy)
    pnts = np.squeeze(pnts)

    ext, conn, simple = sort_points_types(pnts, copy)

    colored = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for p in conn:
        cv2.circle(colored, (p[0], p[1]), 5, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))

    for p in ext:
        cv2.circle(colored, (p[0], p[1]), 5, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
    
    show(colored)
