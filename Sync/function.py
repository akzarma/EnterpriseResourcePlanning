import firebase_admin
from firebase_admin import credentials, db
import os

# print(app.get_access_token())
# data = {'7':'eight'}
#
# # print(root.get(True))
#
# root.child('new').set({"days":[{"day":"Monday","time":[{"facultyLecture":{"batch":"B3","room":"B303","subject":"DBMS"},"time":"0800-0900"}]}],"name":"MPK"})
# root.child('FE').child('ENTC').set({
#     '8':'eight'
# })
cwd = os.getcwd()
print(cwd)
cred = credentials.Certificate(cwd + '/Sync/cert.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://viit-1cbaf.firebaseio.com/'
})


def write_to_firebase(json_string):
    root = db.reference()
    root.child('Student').set(json_string)