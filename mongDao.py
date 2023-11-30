#!/usr/bin/python

#Pyctongo Face Detection

import os, tkMessageBox, pymongo, datetime, pickle
import mongRecog as mrecog
import numpy as np
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.facerecog_database
peopcol = db.people_collection
globcol = db.global_collection
statusCam = False

def startUp():
    if int(globcol.count())==0:
        globcol.insert({'labels_global': []})
    else:
        mrecog.recognizer.load('save.xml')
        mrecog.imagens = pickle.load( open("imagens", "rb"))

def getStatusCam():
    return statusCam

def setStatusCam(on_off):
    statusCam = on_off

def getComboNames():
    combolist = []
    combo_ = peopcol.find()
    for i in combo_:
	combolist.append(i['p_name'])
    return combolist

def insertData(path, p_name, p_age):
    try:
	number = int(peopcol.count())+1
	if getStatusCam():
            path_images= path
	else:
            path_images= [os.path.join(path, f) for f in os.listdir(path)]
        lab_ = globcol.find_one()
        labels = lab_['labels_global']
        labin = len(labels)
	returnQnt = mrecog.prepareImages(path_images, labels, number, getStatusCam())
	for x in range(labin, returnQnt):
	    globcol.update( {}, {'$push': { 'labels_global': number} } )
	peopcol.insert( { "p_id": number, "p_name": p_name, "p_age": p_age, "p_qntimg": returnQnt, "p_insertdate": datetime.datetime.utcnow()} )
    except IOError:
	tkMessageBox.showinfo("Aviso", "Diretorio Invalido")

def updateData(path, p_name):
    try:
        p_id = peopcol.find_one({'p_name': p_name})
	if getStatusCam():
            path_images = path
        else:
            path_images= [os.path.join(path, f) for f in os.listdir(path)]
	returnQnt = mrecog.updateTrain(path_images, p_id['p_id'], getStatusCam())
        for x in range(0, returnQnt):
            globcol.update( {}, {'$push': { 'labels_global': int(p_id['p_id'])} } )
        peopcol.update_one({"p_id": p_id['p_id']}, {"$set": {"p_qntimg": p_id['p_qntimg']+returnQnt}})
        return
    except IOError:
        tkMessageBox.showinfo("Aviso", "Diretorio Invalido")

def recognition(findFace):
    lab_ = globcol.find_one()
    labels = lab_['labels_global']
    lab_recognized, conf = mrecog.faceRecognition(findFace, labels, getStatusCam())
    if conf < 100:
        r = peopcol.find_one({'p_id': lab_recognized})
        print "Reconhecido o usuario ",r['p_name'], " com precisao de : ",100-conf, "%"
    else:
        print "Pessoa nao identificada"
def saveandexit():
    mrecog.recognizer.save('save.xml')
    pickle.dump(mrecog.imagens, open("imagens","wb"))

