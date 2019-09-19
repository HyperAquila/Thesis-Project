from tkinter import *
from PIL import Image
import os


#main
pencere = Tk()
pencere.title("GrabCut Project")
pencere.configure(background="#a3e0ff")
pencere.geometry("300x450+100+100")
pencere.resizable(FALSE,FALSE)

#logo
logo = PhotoImage(file="gelisimLogo.png")
Label(pencere, image = logo, bg = "#a3e0ff").place(x=0, y=0)

#hazırlayan
Label(pencere, text="Hazırlayan ", bg = "#a3e0ff", font = "Bold 14 underline").place(x=105, y=250)
Label(pencere, text="Ali Şükran ÖZDEMİR", bg = "#a3e0ff", font = "Bold 12").place(x=80, y=285)
Label(pencere, text="150403001", bg = "#a3e0ff", font = "Bold 12").place(x=105, y=305)

#komutlar
Label(pencere, text="'n' - Segmentasyon", bg ="#a3e0ff", font = " Bold 8 ").place(x=180, y=5)
Label(pencere, text="'0' - Arka plan belirleme", bg ="#a3e0ff", font = " Bold 8 ").place(x=180, y=23)
Label(pencere, text="'1' - Ön plan belirleme", bg ="#a3e0ff", font = " Bold 8 ").place(x=180, y=43)
Label(pencere, text="'r' - Yenileme", bg ="#a3e0ff", font = " Bold 8 ").place(x=180, y=63)
Label(pencere, text="'s' - Kaydetme", bg ="#a3e0ff", font = " Bold 8 ").place(x=180, y=83)
Label(pencere, text="Çıkmak için 'ESC'", bg ="#a3e0ff", font = " Bold 8" ).place(x=180, y=103)


#buton fonksiyonları
def cikisButton():
    pencere.destroy()

def  grabCut():
    os.system('\"\"C:\\TEZ\\uyg.exe\"\"')


def arkaplanSeffaf():
    img = Image.open('./grabcut_output.png')
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save("./TransparentImage.png", "PNG")
    print('Arkaplan şeffaflaştırıldı\n')


#butonlar

Button(pencere, text ="Arkaplan Şeffaflaştırma", width = 30,bg = "light blue", command = arkaplanSeffaf).place(x=40, y=220)
Button(pencere, text ="GrabCut", width = 30,bg = "light blue", command = grabCut).place(x=40, y=180)
Button(pencere, text ="ÇIKIŞ", width = 10,bg = "#2f8cca", command = cikisButton).place(x=0,y=424)

#main loop
pencere.mainloop()