#!/usr/bin/python

#Pyctongo Face Detection

import cv2, os, tkMessageBox, pymongo, datetime, ttk
import numpy as np
from PIL import Image

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.createFisherFaceRecognizer()
images = []
labels = []

def trainImages(path_images, labPer):
    for imagem_atual in path_images:
        imagem_pil = Image.open(imagem_atual).convert('L')
        imagem = np.array(imagem_pil, 'uint8')
        nbr = int(labPer)
        faces = faceCascade.detectMultiScale(imagem)
        for (x, y, w, h) in faces:
            images.append(imagem[y: y + h, x: x + w])
            labels.append(nbr)
        recognizer.train(images, np.array(labels))

def updateTrain(path_images, labPer):
    l_images=[]
    l_labels=[]
    for imagem_atual in path_images:
        imagem_pil = Image.open(imagem_atual).convert('L')
        imagem = np.array(imagem_pil, 'uint8')
        nbr = int(labPer)
        faces = faceCascade.detectMultiScale(imagem)
        for (x, y, w, h) in faces:
            images.append(imagem[y: y + h, x: x + w])
            labels.append(nbr)
            l_images.append(imagem[y: y + h, x: x + w])
            l_labels.append(nbr)
        recognizer.update(l_images, np.array(l_labels))

def faceRecognition(findFace):
    predict_image_pil = Image.open(findFace).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])        
        return nbr_predicted, conf
