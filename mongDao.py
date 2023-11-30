#!/usr/bin/python

#Pyctongo Face Detection

import os, tkMessageBox, pymongo, datetime, pickle, mongRecog
import mongRecog as mrecog
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.facerecog_database
peopcol = db.people_collection
globcol = db.global_collection

if os.path.isfile('save.xml')==True and os.path.isfile('images')==True:
    mrecog.recognizer.load('save.xml')
    lab_ = globcol.find()
    for i in lab_:
        mrecog.labels = i['labels_global']
    mrecog.images = pickle.load( open("images", "rb"))
else:
    globcol.insert({ 'labels_global': []})

def insertData(path, p_name, p_age):
    try:
	path_images= [os.path.join(path, f) for f in os.listdir(path)]
	mrecog.trainImages(path_images, int(peopcol.count())+1)
	for x in range(0, len(os.listdir(path))):
	    globcol.update( {}, {'$push': { 'labels_global': int(peopcol.count())+1} } )
	peopcol.insert( { "p_id": int(peopcol.count())+1, "p_name": p_name, "p_age": p_age, "p_qntimg": len(os.listdir(path)), "p_insertdate": datetime.datetime.utcnow()} )
	return
    except IOError:
	tkMessageBox.showinfo("Aviso", "Diretorio Invalido")

def updateData(path, p_name):
    try:
	path_images= [os.path.join(path, f) for f in os.listdir(path)]
	p_id = peopcol.find_one({'p_name': p_name})
	mrecog.updateTrain(path_images, p_id['p_id'])
	for x in range(0, len(os.listdir(path))):
	     globcol.update( {}, {'$push': { 'labels_global': int(p_id['p_id'])} } )
	peopcol.update_one({"p_id": p_id['p_id']}, {"$set": {"p_qntimg": p_id['p_qntimg']+len(os.listdir(path))}})
	return
    except IOError:
	tkMessageBox.showinfo("Aviso", "Diretorio Invalido")
    
def getNames():
    combolist = []
    combo_ = peopcol.find()
    for i in combo_:
	combolist.append(i['p_name'])
    return combolist

def recognition(findFace):
    lab_recognized, conf = mrecog.faceRecognition(findFace)
    if conf < 80:
	r = peopcol.find_one({'p_id': lab_recognized})
	print "Reconhecido o usuario ",r['p_name'], " com precisao de : ",100-conf, "%"
    else:
	print "Pessoa nao identificada"
def saveandexit():
    mrecog.recognizer.save('save.xml')
    pickle.dump(mrecog.images, open("images","wb"))

