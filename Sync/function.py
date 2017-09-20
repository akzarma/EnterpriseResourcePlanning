import firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate('cert.json')
app = firebase_admin.initialize_app(cred,{
    'databaseURL':'https://viit-1cbaf.firebaseio.com/'
})
# print(app.get_access_token())
data = {'7':'eight'}
root = db.reference()
# print(root.get(True))

root.child('new').set({"days":[{"day":"Monday","time":[{"facultyLecture":{"batch":"B3","room":"B303","subject":"DBMS"},"time":"0800-0900"}]}],"name":"MPK"})
root.child('FE').child('ENTC').set({
    '8':'eight'
})
