#!/usr/bin/python

#Pyctongo Face Detection

import cv2, os, tkMessageBox, pymongo, datetime, ttk
import numpy as np
from PIL import Image

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.createLBPHFaceRecognizer()

imagens = []

def prepareImages(path_images, labels, number, vid_or_pic):
    for imagem_atual in path_images:
        imagem_pil = Image.open(imagem_atual).convert('L')
        imagem = np.array(imagem_pil, 'uint8')
        faces = faceCascade.detectMultiScale(imagem)
        for (x, y, w, h) in faces:
            imagens.append(imagem[y: y + h, x: x + w])
            labels.append(number)
    return labels

def prepareImagesVid(path_images, labels, number, vid_or_pic):
    for imagem_atual in path_images:
        imagem_pil = Image.open(imagem_atual).convert('L')
        imagem = np.array(imagem_pil, 'uint8')
        faces = faceCascade.detectMultiScale(imagem)
        for (x, y, w, h) in faces:
            imagens.append(imagem[y: y + h, x: x + w])
            labels.append(number)
    return labels


#def updateTrain(path_images, numberLab):
#    l_images=[]
#    l_labels=[]
#    for imagem_atual in path_images:
#        imagem_pil = Image.open(imagem_atual).convert('L')
#        imagem = np.array(imagem_pil, 'uint8')
#  
#        faces = faceCascade.detectMultiScale(imagem)
#        for (x, y, w, h) in faces:
#            l_images.append(imagem[y: y + h, x: x + w])
#            l_labels.append(numberLab)
#        recognizer.update(l_images, np.array(l_labels))

def faceRecognition(findFace, labels, vid_or_pic):
    recognizer.train(imagens, np.array(labels))
    if vid_or_pic ==1:
        predict_image_pil = Image.open(findFace).convert('L')
    else:
	predict_image_pil = findFace
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])

        return nbr_predicted, conf

