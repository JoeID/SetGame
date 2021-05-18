import cv2

img = cv2.imread("test_complet0.png")
img_smol = cv2.resize(img, (800,800))

for i in range(12):
    r = cv2.selectROI(img_smol)
    bounds=list(r)
    for j in range(4):
        bounds[j]=int(bounds[j]*2976/800)
    imCrop = img[int(bounds[1]):int(bounds[1]+bounds[3]), int(bounds[0]):int(bounds[0]+bounds[2])]
    cv2.imwrite("carte{}.png".format(i), imCrop)

cv2.waitKey(0)
cv2.destroyAllWindows()