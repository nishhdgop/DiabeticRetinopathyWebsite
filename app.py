from fpdf import FPDF
import pymongo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cv2
import smtplib
import pyttsx3
import concurrent.futures
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
new_model = load_model('trained_model.h5')
app = Flask(__name__)
global new


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
        future_tasks = {executor.submit(
            textToSpeech, text), executor.submit(typing, text)}
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

def databaseInsert(name, emailId, username, contact, nu):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['iHelp']
    collection = db['iHelp']
    dictionary = {"Name": name, "Email-ID": emailId,
                  "Username": username, "Contact": contact, "Prediction": nu}
    collection.insert_one(dictionary)


predictions = ["Mild", "Moderate",
               "No Diabetic Retinopathy", "Proliferate ", "Severe"]


def predict_new(path, name, emailId, username, contact):
    img = cv2.imread(path)
    RGBImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    RGBImg = cv2.resize(RGBImg, (224, 224))
    plt.imshow(RGBImg)
    image = np.array(RGBImg) / 255.0
    predict = new_model.predict(np.array([image]))
    pred = np.argmax(predict, axis=1)
    a = predictions[pred[0]]
    print(f"\n\n\n\n\n\nPredicted: {a}\n\n\n\n\n\n")
    databaseInsert(name, emailId, username, contact, a)
    file1 = open("basefile.txt", "w")
    mm = f"""
    Greetings from iHelp....
    Your diabetic retinopathy is {a} 
    Thank you for using our service!!!!!

    """
    file1.writelines(mm)
    file1.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    f = open("basefile.txt", "r")
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='C')
    print("Done with pdf")
    pdf.output('report.pdf')
    body = '''Hello,
    This is the body of the email
    sicerely yours
    G.G.
    '''
    sender = 'manik.practicepurpose@gmail.com'
    password = 'xxkvkukpijarqevv'
    receiver = emailId
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'This email has an attacment, a pdf file'
    message.attach(MIMEText(body, 'plain'))
    pdfname = 'report.pdf'
    binary_pdf = open(pdfname, 'rb')
    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload((binary_pdf).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent')
    parallel(f"Your diabetic retinopathy stage is {a}")


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    name = request.form['name']
    emailId = request.form['emailId']
    contact = request.form['contact']
    username = request.form['username']
    print(name, emailId, contact, username)

    imagefile = request.files['imagefile']
    image_path = "images/"+imagefile.filename
    imagefile.save(image_path)
    predict_new(image_path, name, emailId, username, contact)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
