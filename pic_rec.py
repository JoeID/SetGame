import numpy as np
import cv2


def findCaracteristics(contours_img, gray_im):

    # finds the color

    boundaries = [
        ([0,120,0],[100,255,50]),  # green
        ([0,0,120],[100,100,255]),  # red
        ([100,0,50],[255,100,150])  # violet
    ]
    res_color=[]
    colors=["green","red","violet"]
    for (lower, upper) in boundaries:
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(img, lower, upper)
        res_color.append(cv2.countNonZero(mask))
    color = colors[res_color.index(max(res_color))]

    # finds the number a

    thresh = cv2.adaptiveThreshold(gray_im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    a, res= 0, []
    for cnt in contours:
        if len(cnt)>=100:
            a+=1
            res.append(len(cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)))

    # finds the shape

    avg=sum(res)/len(res)

    if avg>=11:
        shape="wave"
    elif avg>=7:
        shape="oval"
    else:
        shape="diamond"

    # finds the fill

    fill=len([cnt for cnt in contours_img if len(cnt)>=4])/a
    if fill>4:
        fill="striped"
    elif fill==1:
        fill="full"
    else:
        if max(res_color)/a>=15000:
            fill="full"
        else:
            fill="empty"

    return color, a, shape, fill


def parties(k, E): #renvoie les parties de E de cardinal k
    if not E:
        if k==0:
            return [[]]
        else:
            return []
    else:
        h, t = E[0], E[1:]
        b = parties(k-1,t)
        return parties(k, t) + list(map(lambda x:[h]+x, b))


def resolution(set):
    res=[]
    for (carte1,carte2,carte3) in parties(3, set):
        for i in range(4):
            if not ((carte1[i]==carte2[i] and carte1[i]==carte3[i]) or
                    (carte1[i]!=carte2[i] and carte2[i]!=carte3[i] and carte1[i]!=carte3[i])):
                break
        else:
            res.append((carte1,carte2,carte3))
    return res


img_set = cv2.imread("test_complet0.png")

set=[]
for i in range(12):
    name="carte{}.png".format(i)
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(gray,127,255,1)
    contours2, hierarchy2 = cv2.findContours(thresh, 1, 2)

    set.append(findCaracteristics(contours2, gray))

resol = resolution(set)
print(set, resol)
colors = [(0,0,255),(0,255,0),(255,0,0),(255,255,0),(255,0,255),(0,255,255)]

img_set = cv2.resize(img_set, (800, 800))
for d in range(len(resol)):
    for carte in resol[d]:
        i = set.index(carte)
        x, y = i%4, i//4
        x, y = int((x+1/2)*800/4), int((y+1/2)*800/3)
        cv2.circle(img_set, (x, y), 150-10*d, colors[d], 10)

cv2.imshow("Jeu de Set", img_set)

cv2.waitKey(0)
cv2.destroyAllWindows()
