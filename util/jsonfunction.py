import os
import json


def getJson(filePath):
    directory = "/".join(filePath.split('/')[:-1]) + "/"
    name = filePath.split('/')[-1]
    files = os.listdir(directory)
    #print(directory, name)
    for file in files:
        if name in file:
            with open(os.path.join(directory, file)) as jsonFile:
                data = json.load(jsonFile)
            return data
    return []


def toJson(directory, name, data):
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(data, f, indent=2)


def appendJson(directory, name, data):
    datastore = getJson(directory, name)
    if name == "verifiedLol":
        del data['birthdate']
        del data['confirm_password']
        mail = data['email'][0] + "@" + data['email'][1]
        data['email'] = mail

    datastore.append(data)
    with open(os.path.join(directory, name + ".json"), 'w') as f:
        json.dump(datastore, f, indent=2)


def jsonPrint(dataName, data):
    print(dataName + ":", json.dumps(data, indent=2))
