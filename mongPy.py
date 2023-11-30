#!/usr/bin/python
#Pyctongo Face Detection

import Tkinter, tkMessageBox, tkFileDialog, ttk, cv2, time
import mongDao as dao
from PIL import ImageTk, Image

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def app():
    dao.startUp()

    # Frames
    def blankFrame(frame):
        slaves = frame.pack_slaves()
        for widget in slaves:
            widget.destroy()
    def clearFrames():
	blankFrame(frame1)
	blankFrame(frame2)
	blankFrame(frame3)
        closeWebcam()

    # Camera
    def openWebcam():
        def webcamActivated():
            _, videoframe = cap.read()
            videoframe = cv2.flip(videoframe, 1)
            cv2image = cv2.cvtColor(videoframe, cv2.COLOR_BGR2RGBA)
            global imageGray
            imageGray = cv2.cvtColor(videoframe, cv2.COLOR_BGR2GRAY)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lbvideo.imgtk = imgtk
            lbvideo.configure(image=imgtk)
            lbvideo.after(1, webcamActivated)
        global framevideo
	framevideo = Tkinter.Frame(frame3)
	framevideo.pack()
	lbvideo = Tkinter.Label(framevideo)
	lbvideo.pack()
	global cap
	cap = cv2.VideoCapture(0)
	cap.set(3, 500)
	cap.set(4, 300)
	dao.statusCam=True
	global framebutvid
	framebutvid = Tkinter.Frame(frame3)
	framebutvid.pack()
	insertButtonVid(framebutvid)
	webcamActivated()
    def closeWebcam():
	scam = dao.getStatusCam()
	if scam == True:
	    dao.statusCam=False
	    framevideo.destroy()
	    blankFrame(frame3)
	    cap.release()
    # Botao Captura
    def insertButtonVid(framebutvid):
        try:
            tbname.get()
            blankFrame(framebutvid)
	    btfrm3=Tkinter.Button(framebutvid, text="Capturar", height=5, width=15, command=getScreen)
	    btfrm3.pack()
	except:
	    try:
                combobox.get()
                blankFrame(framebutvid)
	        btfrm3=Tkinter.Button(framebutvid, text="Capturar", height=5, width=15, command=getScreen)
	        btfrm3.pack()
	    except:
	        return 0

    def getScreen():
        faces = faceCascade.detectMultiScale(imageGray)
        try:
	    for f in faces:
                x, y, w, h = [ v for v in f ]
	        x, y, w, h = (x-45), (y-40), (w+90), (h+60)
	        findFace = cv2.resize(imageGray[y:y+h, x:x+w], (300,300))
                try:
                    tbname.get()
                    dao.insertData(findFace, tbname.get(), tbage.get())
                except:
	            dao.updateData(findFace, combobox.get())
	except:
            print "Nao foi possivel capturar a imagem"

    # Frame1
    def selectData():
	if option.get()==1:
	    blankFrame(frame2)
	    def showFields():
		if tbname.get()!="" and tbage.get()!="":
		    if not dao.getStatusCam():
			path = tkFileDialog.askdirectory(parent=mainWin,initialdir="./faces",title='Escolha de diretorio')
			if path != "":
			    dao.insertData(path, tbname.get(), tbage.get())
			    clearFrames()
		    else:
			clearFrames()
		else:
		    tkMessageBox.showinfo("Aviso", "Campo vazio")
	    lbname=Tkinter.Label(frame2, text="Nome:", width=50)
            global tbname
	    tbname=Tkinter.Entry(frame2, width=50)
	    lbage=Tkinter.Label(frame2, text="Idade", width=50)
            global tbage
	    tbage=Tkinter.Entry(frame2, width=50)
	    lbname.pack(fill=Tkinter.X, ipady=10)
	    tbname.pack(fill=Tkinter.X, ipady=8)
	    lbage.pack(fill=Tkinter.X, ipady=10)
	    tbage.pack(fill=Tkinter.X, ipady=8)
	    Tkinter.Label(frame2, text=" ").pack(fill=Tkinter.X, ipady=10)
	    btfrm2=Tkinter.Button(frame2, text="Ok", width=15, command=showFields)
	    btfrm2.pack(fill=Tkinter.Y, ipady=30)
            if dao.getStatusCam()==True:
	        insertButtonVid(framebutvid)
	elif option.get()==2:
	    blankFrame(frame2)
	    def showFields():
		if combobox.get():
		    try:
			if not dao.getStatusCam():
			    path = tkFileDialog.askdirectory(parent=mainWin,initialdir="./faces",title='Escolha de diretorio')
                            if path != "":
			        dao.updateData(path, combobox.get())
                                clearFrames()
			else:
			    clearFrames()
		    except:
			return 0			
		else:
		    tkMessageBox.showinfo("Aviso", "Campo vazio")
	    global combobox
	    combobox = ttk.Combobox(frame2, textvariable="Combo")
	    combo_ = dao.getComboNames()
	    combobox['values'] = combo_
	    combobox.pack(ipady=10, expand = "yes")
	    btfrm2=Tkinter.Button(frame2, text="Confirmar", command=showFields)
	    btfrm2.pack(ipady=30, ipadx=33, expand = "yes")
	    if dao.getStatusCam()==True:
	        insertButtonVid(framebutvid)

    def getOptionInsert():
        return option.get()

    def insertFaces():
	rb1 = Tkinter.Radiobutton(frame1, text="Criar novo", variable=option, height=6, width=180, value=1, command=getOptionInsert)
	rb1.pack()
	rb2 = Tkinter.Radiobutton(frame1, text="Adicionar existente", variable=option, height=6, width=180, value=2)
	rb2.pack()
	btfrm1 = Tkinter.Button(frame1, text="Ok", height=5, width=15, command=selectData)
	btfrm1.pack()

    def findOutPerson():
	blankFrame(frame1)
	blankFrame(frame2)
	try:
            blankFrame(framebutvid)
	except:
            print ""
	try:
	    if dao.statusCam == False:
		findFace = tkFileDialog.askopenfilename(parent=mainWin,initialdir="./faces",title='Escolha de arquivo')
		if findFace != "":
		    dao.recognition(findFace)
            else:
                faces = faceCascade.detectMultiScale(imageGray)
                try:
	            for f in faces:
			x, y, w, h = [ v for v in f ]
		        try:
		            x, y, w, h = (x-45), (y-40), (w+90), (h+60)
	                    findFace = cv2.resize(imageGray[y:y+h, x:x+w], (300,300))
	                    dao.recognition(findFace)
		        except:
		            print "Imagem Fora do alcance"
	        except:
                    print "Nao foi possivel capturar a imagem"
        except IOError:
            tkMessageBox.showinfo("Aviso", "Diretorio Invalido!")

    def saveandexit():
        dao.saveandexit()
        mainWin.quit()

    mainWin = Tkinter.Tk()
    global option
    option=Tkinter.IntVar()
    mainWin.title("MonPycture: Facial Recognition")
    mainWin.geometry("750x350+100+100")
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

    videoMenu = Tkinter.Menu(menu)
    menu.add_cascade(label="Video Camera", menu=videoMenu)
    videoMenu.add_command(label="Utilizar Webcam", command=openWebcam)
    videoMenu.add_command(label="Fechar Webcam", command=closeWebcam)

    clearMenu = Tkinter.Menu(menu)
    menu.add_cascade(label="Limpar", menu=clearMenu)
    clearMenu.add_command(label="Limpar tudo", command=clearFrames)

    pannel = Tkinter.PanedWindow(mainWin)
    pannel.pack(fill="both", expand="yes", padx=3)
    frame1 = Tkinter.Frame(pannel, bd=1, relief=Tkinter.SOLID)
    frame2 = Tkinter.Frame(pannel, bd=1, relief=Tkinter.SOLID)
    frame3 = Tkinter.Frame(pannel, bd=1, relief=Tkinter.SOLID)
    pannel.add(frame1, width=180)
    pannel.add(frame2, width=180)
    pannel.add(frame3, width=180)
    statusCam=False
    mainWin.mainloop()
app()
