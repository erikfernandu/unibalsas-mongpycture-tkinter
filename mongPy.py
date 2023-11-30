#!/usr/bin/python
#Pyctongo Face Detection

import Tkinter, tkMessageBox, tkFileDialog, ttk, mongDao
import mongDao as dao
from PIL import ImageTk, Image

class Window():
    def __init__(self):
        def getValue():
            return option.get()
        def blankFrames(frames):
            slaves = frames.pack_slaves()
            for widget in slaves:
                widget.pack_forget()
        def selectData():
            if option.get()==1:
                blankFrames(frame2)
                def showFields():
                    if tbname.get()!="" and tbage.get()!="":
                        path = tkFileDialog.askdirectory(parent=mainWin,initialdir="./addfaces",title='Escolha de diretorio')
                        blankFrames(frame1)
                        blankFrames(frame2)
                        blankFrames(frame3)
                        dao.insertData(path, tbname.get(), tbage.get())
                    else:
                        tkMessageBox.showinfo("Aviso", "Campo vazio")
                lbname=Tkinter.Label(frame2, text="Nome:", width=50)
                tbname=Tkinter.Entry(frame2, width=50)
                lbage=Tkinter.Label(frame2, text="Idade", width=50)
                tbage=Tkinter.Entry(frame2, width=50)
                lbname.pack(fill=Tkinter.X, ipady=10)
                tbname.pack(fill=Tkinter.X, ipady=8)
                lbage.pack(fill=Tkinter.X, ipady=10)
                tbage.pack(fill=Tkinter.X, ipady=8)
                Tkinter.Label(frame2, text=" ").pack(fill=Tkinter.X, ipady=10)
                btfrm2=Tkinter.Button(frame2, text="Ok", width=15, command=showFields)
                btfrm2.pack(fill=Tkinter.Y, ipady=30)
            elif option.get()==2:
                blankFrames(frame2)
                def showFields():
                    if combobox.get():
                        path = tkFileDialog.askdirectory(parent=mainWin,initialdir="./addfaces",title='Escolha de diretorio')
                        blankFrames(frame1)
                        blankFrames(frame2)
                        dao.updateData(path, combobox.get())
                    else:
                        tkMessageBox.showinfo("Aviso", "Campo vazio")
                combobox = ttk.Combobox(frame2, textvariable="Combo")
                combo_ = dao.getNames()
                combobox['values'] = combo_
                combobox.pack(ipady=10, expand = "yes")
                btfrm2=Tkinter.Button(frame2, text="Confirmar", command=showFields)
                btfrm2.pack(ipady=30, ipadx=33, expand = "yes")

        def insertFaces():
            rb1 = Tkinter.Radiobutton(frame1, text="Criar novo", variable=option, height=6, width=180, value=1, command=getValue)
            rb1.pack()
            rb2 = Tkinter.Radiobutton(frame1, text="Adicionar existente", variable=option, height=6, width=180, value=2)
            rb2.pack()
            btfrm1 = Tkinter.Button(frame1, text="Ok", height=5, width=15, command=selectData)
            btfrm1.pack()

        def findOutPerson():
            blankFrames(frame1)
            blankFrames(frame2)
            blankFrames(frame3)
            try:
                findFace = tkFileDialog.askopenfilename(parent=mainWin,initialdir="./addfaces",title='Escolha de arquivo')
                dao.recognition(findFace)
                img = ImageTk.PhotoImage(Image.open("./addfaces/erik.gif"))
                can = Tkinter.Canvas(frame3)
                can.create_image(190,150, image = img)
                can.pack(side = "bottom", fill = "both", expand = "yes")
                frame3.update()
            except IOError:
                tkMessageBox.showinfo("Aviso", "Diretorio Invalido!")

        def saveandexit():
            dao.saveandexit()
            mainWin.quit()

        mainWin = Tkinter.Tk()
        option=Tkinter.IntVar()
        mainWin.title("MonPycture: Facial Recognition")
        mainWin.geometry("750x300+100+100")
        menu = Tkinter.Menu(mainWin)
        mainWin.config(menu=menu)

        insertMenu = Tkinter.Menu(menu)
        menu.add_cascade(label="Arquivos", menu=insertMenu)
        insertMenu.add_command(label="Inserir Faces", command=insertFaces)
        insertMenu.add_separator()
        insertMenu.add_command(label="Sair", command=saveandexit)

        reconMenu = Tkinter.Menu(menu)
        menu.add_cascade(label="Reconhecimento", menu=reconMenu)
        reconMenu.add_command(label="Reconhecer Imagem", command=findOutPerson)
        reconMenu.add_command(label="Salvar XML")
        reconMenu.add_command(label="Carregar XML")

        pannel = Tkinter.PanedWindow(mainWin)
        pannel.pack(fill="both", expand="yes", padx=3)
        frame1 = Tkinter.Frame(pannel, bd=1, relief=Tkinter.SOLID)
        frame2 = Tkinter.Frame(pannel, bd=1, relief=Tkinter.SOLID)
        frame3 = Tkinter.Frame(pannel, bd=1, relief=Tkinter.SOLID)
        pannel.add(frame1, width=180)
        pannel.add(frame2, width=180)
        pannel.add(frame3, width=180)

        mainWin.mainloop()
Window()
