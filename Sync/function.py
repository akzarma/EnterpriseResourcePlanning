import firebase_admin
from firebase_admin import credentials, db
import os

# data = {'7':'eight'}
#
#
# root.child('new').set({"days":[{"day":"Monday","time":[{"facultyLecture":{"batch":"B3","room":"B303","subject":"DBMS"},"time":"0800-0900"}]}],"name":"MPK"})
# root.child('FE').child('ENTC').set({
#     '8':'eight'
# })
cwd = os.getcwd()
cred = credentials.Certificate(cwd + '/Sync/cert.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://viit-1cbaf.firebaseio.com/'
})


def write_to_firebase(json_string,next_child):
    root = db.reference()
    root.child(next_child).set(json_string)