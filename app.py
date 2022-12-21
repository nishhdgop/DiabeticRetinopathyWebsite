import smtplib
import mysql.connector
import pyttsx3
import concurrent.futures
import sys
from time import sleep
from flask import Flask,render_template,request
from tensorflow.keras.models import load_model
new_model = load_model('trained_model.h5')
app = Flask(__name__) 
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def typing(text):
    for char in text:
        sleep(0.04)
        sys.stdout.write(char)
        sys.stdout.flush()

def textToSpeech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 220)
    engine.say(text)
    engine.runAndWait()
    del engine

def parallel(text):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_tasks = {executor.submit(textToSpeech, text), executor.submit(typing, text)}
        for future in concurrent.futures.as_completed(future_tasks):
            try:
                data = future.result()
            except Exception as e:
                print(e)

                
def mail(receiver_mail_id, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("manik.practicepurpose@gmail.com", "xxkvkukpijarqevv")
    s.sendmail("manik.practicepurpose@gmail.com", receiver_mail_id, message)
    s.quit()

predictions=["Mild","Moderate","No_DR","Proliferate_DR","Severe"] 
def predict_new(path):
    img = cv2.imread(path)

    RGBImg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    RGBImg= cv2.resize(RGBImg,(224,224))
    plt.imshow(RGBImg)
    image = np.array(RGBImg) / 255.0

    predict=new_model.predict(np.array([image]))
    pred=np.argmax(predict,axis=1)
    
    
    a=predictions[pred[0]]
    print(f"\n\n\n\n\n\nPredicted: {a}\n\n\n\n\n\n")
    mail("nischithtn@gmail.com",f"""
    Greetings from iHelp....
    Your diabetic retinopathy is {a} 
    Thank you for using our service!!!!!

    """)
    parallel(f"Your diabetic retinopathy stage is {a}")
    

@app.route('/',methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def predict():
    imagefile = request.files['imagefile'] 
    image_path = "./images/"+imagefile.filename 
    imagefile.save(image_path)
    predict_new(image_path)
    return render_template('index.html') 

if __name__ == '__main__':
    app.run(port=3000,debug=True)  