'''
===============================================================================
Tuş '0' - Kesin arka plan alanlarını seçmek için
Tuş '1' - Kesin ön plan alanlarını seçmek için
Tuş 'n' - Yeniden segmentasyon yapmak için
Tuş 'r' - Kurulumu sıfırlamak için
Tuş 's' - Sonuçları kaydetmek için
===============================================================================
'''

import numpy as np
import cv2 as cv

BLUE = [255,0,0]        #  dikdörtgen rengi
BLACK = [0,0,0]         #  BG (Background-Arkaplan)
WHITE = [255,255,255]   #  FG (Foreground-Önplan)

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}

# flag ayarlama
rect = (0,0,1,1)
drawing = False         # eğrilerin çizimi için flag
rectangle = False       # dikdörtgen çizimi için flag
rect_over = False       # dikdörtgen kontrolü için flag
rect_or_mask = 100      # dikdörtgen veya maske modu seçmek için flag
value = DRAW_FG         # Ön plana ilk çizilen çizim
thickness = 2           # fırça kalınlığı



def onmouse(event,x,y,flags,param):
    global img,img2,drawing,value,mask,rectangle,rect,rect_or_mask,ix,iy,rect_over

    # Dikdörtgen çizimi
    if event == cv.EVENT_RBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv.EVENT_MOUSEMOVE:
        if rectangle == True:
            img = img2.copy()
            cv.rectangle(img,(ix,iy),(x,y),BLUE,2)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
            rect_or_mask = 0

    elif event == cv.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        cv.rectangle(img,(ix,iy),(x,y),BLUE,2)
        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
        rect_or_mask = 0
        print("Başka bir değişiklik yapmayıncaya kadar şimdi 'n' tuşuna birkaç kez basın \n")

    # Resim üzerinde oynama yapma

    if event == cv.EVENT_LBUTTONDOWN:
        if rect_over == False:
            print("ilk dikdörtgen çizimi \n")
        else:
            drawing = True
            cv.circle(img,(x,y),thickness,value['color'],-1)
            cv.circle(mask,(x,y),thickness,value['val'],-1)

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.circle(img,(x,y),thickness,value['color'],-1)
            cv.circle(mask,(x,y),thickness,value['val'],-1)

    elif event == cv.EVENT_LBUTTONUP:
        if drawing == True:
            drawing = False
            cv.circle(img,(x,y),thickness,value['color'],-1)
            cv.circle(mask,(x,y),thickness,value['val'],-1)

if __name__ == '__main__':

    img = cv.imread('grabCut.png')
    img2 = img.copy()                               # orijinal görüntünün kopyası
    mask = np.zeros(img.shape[:2],dtype = np.uint8) # PR_BG için başlatılan maske
    output = np.zeros(img.shape,np.uint8)           # gösterilecek çıkış resmi

    # giriş çıkış pencereleri
    cv.namedWindow('output')
    cv.namedWindow('input')
    cv.setMouseCallback('input',onmouse)
    cv.moveWindow('input',img.shape[1]+10,90)

    print(" Talimatlar: \n")
    print(" Farenin sağ tuşunu kullanarak nesnenin etrafına bir dikdörtgen çizin \n")

    while(1):

        cv.imshow('output',output)
        cv.imshow('input',img)
        k = cv.waitKey(1)

        # tuş bağlantıları
        if k == 27:         # çıkmak için ESC
            break

        elif k == ord('0'): # Arkaplan çizimi
            print(" sol fare tuşuyla arka plan bölgelerini işaretle \n")
            value = DRAW_BG

        elif k == ord('1'): # Önplan çizimi
            print(" sol fare tuşuyla ön plandaki bölgeleri işaretleyin \n")
            value = DRAW_FG

        elif k == ord('s'): # resmi kaydetme
            bar = np.zeros((img.shape[0],5,3),np.uint8)
            res = np.hstack((img2,bar,img,bar,output))
            cv.imwrite('grabcut_output.png',output)
            print(" Sonuç resim olarak kaydedildi \n")

        elif k == ord('r'): # Her şeyi sıfırlama(resim üzerinde yapılan oynamalar için)
            print("sıfırlanıyor \n")
            rect = (0,0,1,1)
            drawing = False
            rectangle = False
            rect_or_mask = 100
            rect_over = False
            value = DRAW_FG
            img = img2.copy()
            mask = np.zeros(img.shape[:2],dtype = np.uint8) # PR_BG için başlatılan maske
            output = np.zeros(img.shape,np.uint8)           # gösterilecek çıkış resmi

        elif k == ord('n'): # segmentasyon yapma
            print(""" Daha hassas rötuşlar için, 0-3 tuşlarına bastıktan sonra ön ve arka planı işaretleyin
            ve tekrar basın 'n' \n""")

            if (rect_or_mask == 0):         # grabcut dikdörtgen ile kapma
                bgdmodel = np.zeros((1,65),np.float64)
                fgdmodel = np.zeros((1,65),np.float64)
                cv.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv.GC_INIT_WITH_RECT)
                rect_or_mask = 1

            elif rect_or_mask == 1:         # grabcut maske ile kapma
                bgdmodel = np.zeros((1,65),np.float64)
                fgdmodel = np.zeros((1,65),np.float64)
                cv.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv.GC_INIT_WITH_MASK)

        mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
        output = cv.bitwise_and(img2,img2,mask=mask2)


    cv.destroyAllWindows()

