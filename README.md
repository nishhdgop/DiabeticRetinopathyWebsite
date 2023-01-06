# Hackzon 2023 macBlockers 
# i-Help : Diabetic Retinopathy Detection

India is often referred to as the ‘Diabetes Capital of the World' as it accounts for a whopping 17% of the total diabetes patients in the world. There are currently close to 80 million people with diabetes in India and this number is set to rise to 135 million by 2045.

With the rise of diabetes, the risks associated with diabetes has also been leading to complications like Diabetic Retinopathy.

Diabetic retinopathy is an eye condition that can cause vision loss and blindness in people who have diabetes. It affects blood vessels in the retina (the light-sensitive layer of tissue in the back of the eye). For patients with diabetes, it is important to get a comprehensive dilated eye exam at least once a year. 

Diabetic retinopathy is best diagnosed with a comprehensive dilated eye exam. Exams like Optical Coherence Tomography (OCT) are taken for this purpose. However, this requies expensive OCT machines and expertise to provide the required diagnosis, both of which are lacking in rural and small town areas.  


*iHelp* is our attempt to resolve this problem. With the help of Deep Learning, VGG algorithms and Machine training, we have built an inexpensive and convenient alternative to costly equipment like OCT machines. 

This code can be implemented through regular eye scanners for an early detection of Diabetic Retinopathy, thus preventing possible permanent blindness due to diabetic complications. 

## Tools used for development :

### Frontend - 
HTML, CSS, Flask

### Backend -
MongoDB, IPFS, CNN, TensorFlow, Keras, Moralis

### Our Features : 
- Detection of 5 stages of Diabetic Retinopathy.
- Interactive UI-based web-app
- A chatbot on our web-app for service assistance and ease of usage.
- Generated DR report is sent to patient’s email.
- This report is also backed up on our IPFS web3 storage.
- Shows location of nearest eye hospital.

#### Implementation :
- The eye scan is fed into our model through the interface.
- This scan is analysed and a DR detection report is generated, based on our dataset of about 3,600 images of DR retina scans from IEEE.
- The detailed report is sent to the patient's email, and stored in MongoDB.
- All our data in MongoDB is backed up in our decentralised IPFS web3 storage.
- Google Maps API has been used for showing the nearest eye hospital as a suggestion to the patient, based on the current location of the user.
- If the patient has any queries, they can get the required answers through our chatbot on our web-app.

#### Output Screenshots:
Output 1:
i-Help web app user interface

![UI1 (1)](https://user-images.githubusercontent.com/108075033/210940143-c68439fa-9570-4e1c-920d-ae6ba9c09a68.png)

Output 2:
User interface 2

![UI1 (2)](https://user-images.githubusercontent.com/108075033/210940242-4633ea3c-de61-4d13-9637-b9429d3cdcff.png)

Output 3:
Nearest hospital location

![UI1 (3)](https://user-images.githubusercontent.com/108075033/210940312-c0564bdd-9e40-45c9-9321-c9d47993f540.png)

Output 4:
ChatBot implementation in the web app.

![UI1_chatbot](https://user-images.githubusercontent.com/108075033/210940340-7525c9cb-2b17-4a05-ab47-3bbc2698f2db.png)

Output 5:
Diabetic Retinopathy Detection by uploading the eye scan image.

![UI1_prediction](https://user-images.githubusercontent.com/108075033/210940360-10ab66db-3f36-4f2c-8892-7c1e943b89eb.png)

Output 6:
MongoDb database to store user information and the ipfs report pdf url.

![UI1_mongodb](https://user-images.githubusercontent.com/108075033/210940391-9e015c4f-0acd-4cd8-98a9-1c298f96a501.png)

Output 7:
The email is generateed once the prediction happens from the image uploaded by the user. The email consists of an attachment of the medical report generated.

![UI1_email](https://user-images.githubusercontent.com/108075033/210940453-570fe8e3-70de-4fb6-8104-00cafd6eeab0.png)

Output 8:
The generated report after prediction stored on the ipfs web3 storage.

![ipfs_pdf](https://user-images.githubusercontent.com/108075033/210940474-7fd60b29-0d76-47e7-873d-24646cddc213.png)








