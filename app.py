from fpdf import FPDF
import pymongo
import matplotlib.pyplot as plt
# import pandas as pd
from moralis import evm_api 
from base64_pdf import BASE_64
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

def databaseInsert(name, emailId, username, contact, nu,url):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['iHelp']
    collection = db['iHelp']
    dictionary = {"Name": name, "Email-ID": emailId,
                  "Username": username, "Contact": contact, "Prediction": nu,"IPFS_URL":url}
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
    
    file1 = open("basefile.txt", "w")
  
    if(a=="Mild"):
        mm =   f"""
                        DIABETIC RETINOPATHY report by i-Help

     Patient name:{name}
     Age: {username}
     Email id:{emailId}
     Contact no:{contact}

     Diagnosis:
     1. Retina scan shows signs of {a} DR.

     Further advice for treatment: 
     1. Patient is advised to keep sugar levels in check.
     2. Take a glycosylated haemoglobin or haemoglobinn A1C test.
     3.Excercise regularly and lose excess weight.
     4.Pay attention to vision changes.

     a) For further advice the patient can visit the nearest eye hospital 
        to the current location(as displayed on the website).
     b) To contact us visit our i-Help web app.
     c) Incase this report is lost, a copy of this report can be found 
        on our IPFS Web3 storage.

    """
    elif(a=="Moderate"):
        mm =  f"""
                        DIABETIC RETINOPATHY report by i-Help

     Patient name:{name}
     Age: {username}
     Email id:{emailId}
     Contact no:{contact}

     Diagnosis:
     1. Retina scan shows signs of {a} DR.

     Further advice for treatment: 
     1. Patient is advised to keep sugar levels in check.
     2. Take a glycosylated haemoglobin or haemoglobinn A1C test.
     3.Excercise regularly and lose excess weight.
     4.Pay attention to vision changes

     a) For further advice the patient can visit the nearest eye hospital 
        to the current location(as displayed on the website).
     b) To contact us visit our i-Help web app.
     c) Incase this report is lost, a copy of this report can be found 
        on our IPFS Web3 storage.

        """
    elif(a=="No Diabetic Retinopathy"):
        mm =  f"""
                        DIABETIC RETINOPATHY report by i-Help

     Patient name:{name}
     Age: {username}
     Email id:{emailId}
     Contact no:{contact}

     Diagnosis:
     1. Retina scan shows signs of {a} DR.
     2. Patient is advised to excercise regularly.
     
     Further advice for treatment:
     a) For further advice the patient can visit the nearest eye hospital 
        to the current location(as displayed on the website).
     b) To contact us visit our i-Help web app.
     c) Incase this report is lost, a copy of this report can be found 
        on our IPFS Web3 storage.

        """ 
    elif(a=="Proliferate "):
        mm = f"""
                        DIABETIC RETINOPATHY report by i-Help

     Patient name:{name}
     Age: {username}
     Email id:{emailId}
     Contact no:{contact}

     Diagnosis:
     1. Retina scan shows signs of {a} DR.
     2. Patient is stronlgy advised to meet an opthalmologist.
     3. Patient will require laser treatment or surgery to avoid losing vision.

     Further advice for treatment:
     a) For further advice the patient can visit the nearest eye hospital 
        to the current location(as displayed on the website).
     b) To contact us visit our i-Help web app.
     c) Incase this report is lost, a copy of this report can be found 
        on our IPFS Web3 storage.

        """
    elif(a=="Severe"):
        mm = f"""
                        DIABETIC RETINOPATHY report by i-Help

     Patient name:{name}
     Age: {username}
     Email id:{emailId}
     Contact no:{contact}

     Diagnosis:
     1. Retina scan shows signs of {a} DR.
     2.Patient is advised to consult an opthalmologist as soon as possible.
     3.Patient might require laser treatment or surgery.
     
     Further advice for treatment:
     a) For further advice the patient can visit the nearest eye hospital 
        to the current location(as displayed on the website).
     b) To contact us visit our i-Help web app.
     c) Incase this report is lost, a copy of this report can be found 
        on our IPFS Web3 storage.

        """

    file1.writelines(mm)
    file1.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    f = open("basefile.txt", "r")
    for x in f:
        pdf.cell(200, 8, txt=x, ln=.8, align='L')
    print("Done with pdf")
    ipfsurl=ipfsupload()
    databaseInsert(name, emailId, username, contact, a,ipfsurl)
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

def ipfsupload():
    api_key="zCeUElAUJESksh44iZAMQnKVzrzqO5rkmoHVxIK06XL1qJdHDVFADZJ5V6gPNNdI"
    body=[
    {
        "path":"report.pdf",
        "content":BASE_64,
    }
    ]
    result=evm_api.ipfs.upload_folder(
    api_key=api_key,
    body=body,
    )
    return result[0]["path"]
   

if __name__ == '__main__':
    app.run(port=3000, debug=True)
