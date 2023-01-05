def databaseInsert(name, emailId, username, contact, nu):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['iHelp']
    collection = db['iHelp']
    dictionary = {"Name": name, "Email-ID": emailId,
                  "Username": username, "Contact": contact, "Prediction": nu}
    collection.insert_one(dictionary)


predictions = ["Mild", "Moderate",
               "No Diabetic Retinopathy", "Proliferate ", "Severe"]