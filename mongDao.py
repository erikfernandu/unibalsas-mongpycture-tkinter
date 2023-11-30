#!/usr/bin/python

#Pyctongo Face Detection

import os, tkMessageBox, pymongo, datetime, pickle, mongRecog
import mongRecog as mrecog
import numpy as np
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.facerecog_database
peopcol = db.people_collection
globcol = db.global_collection
statusCam = False
insertedPerson=None

def startUp():
    if int(globcol.count())==0:
        globcol.insert({'labels_global': []})
#        globcol.insert({'images_global': []})
    else:
        mrecog.recognizer.load('save.xml')
        mrecog.imagens = pickle.load( open("imagens", "rb"))

def getInsertedPerson():
    return insertedPerson

def setInsertedPerson(newUser):
    insertedPerson=newUser

def getComboNames():
    combolist = []
    combo_ = peopcol.find()
    for i in combo_:
	combolist.append(i['p_name'])
    return combolist

def insertData(path, p_name, p_age):
    try:
	number = int(peopcol.count())+1
	path_images= [os.path.join(path, f) for f in os.listdir(path)]
        lab_ = globcol.find()
        for i in lab_:
            labels = i['labels_global']
	labin = len(labels)
	returnLab = mrecog.prepareImages(path_images, labels, number, 1)
        for x in range(labin, len(returnLab)):
	    globcol.update( {}, {'$push': { 'labels_global': number} } )
	peopcol.insert( { "p_id": number, "p_name": p_name, "p_age": p_age, "p_qntimg": len(os.listdir(path)), "p_insertdate": datetime.datetime.utcnow()} )
    except IOError:
	tkMessageBox.showinfo("Aviso", "Diretorio Invalido")

def insertDataVid(path_images, p_name, p_age):
#    q = getInsertedPerson()
#    if q == None:
#        number = int(peopcol.count())+1
#        setInsertPerson(p_name)
#    else:
    number = int(peopcol.count())
    lab_ = globcol.find()
    for i in lab_:
        labels = i['labels_global']
    labin = len(labels)
    returnLab = mrecog.prepareImages(path_images, labels, number, 2)
    for x in range(labin, len(returnLab)):
        globcol.update( {}, {'$push': { 'labels_global': number} } )
    peopcol.insert( { "p_id": number, "p_name": p_name, "p_age": p_age, "p_qntimg": len(os.listdir(path)), "p_insertdate": datetime.datetime.utcnow()} )

#def updateData(path, p_name):
#    try:
#        path_images= [os.path.join(path, f) for f in os.listdir(path)]
#        p_id = peopcol.find_one({'p_name': p_name})
#        mrecog.updateTrain(path_images, p_id['p_id'])
#        for x in range(0, len(os.listdir(path))):
#            globcol.update( {}, {'$push': { 'labels_global': int(p_id['p_id'])} } )
#        peopcol.update_one({"p_id": p_id['p_id']}, {"$set": {"p_qntimg": p_id['p_qntimg']+len(os.listdir(path))}})
#        return
#    except IOError:
#        tkMessageBox.showinfo("Aviso", "Diretorio Invalido")

def recognition(findFace):
    lab_ = globcol.find()
    for i in lab_:
        labels = i['labels_global']
    if str(type(findFace)) == "<type 'numpy.ndarray'>":
	vid_or_pic = 2
    else:
	vid_or_pic = 1
    lab_recognized, conf = mrecog.faceRecognition(findFace, labels, vid_or_pic)
    if conf < 80:
	r = peopcol.find_one({'p_id': lab_recognized})
	print "Reconhecido o usuario ",r['p_name'], " com precisao de : ",100-conf, "%"
    else:
	print "Pessoa nao identificada"
def saveandexit():
    mrecog.recognizer.save('save.xml')
    pickle.dump(mrecog.imagens, open("imagens","wb"))

