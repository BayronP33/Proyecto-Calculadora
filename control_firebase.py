# control_firebase.py

import firebase_admin
from firebase_admin import credentials, firestore, db

# Inicializar la aplicación Firebase
cred = credentials.Certificate("D:/PROYECTO_CALCULADORA/TESTPOO.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://calculadora-c74f7-default-rtdb.firebaseio.com/'
})

# Inicializar Firestore y Realtime Database
firestore_db = firestore.client()
realtime_db = db.reference("/")

def actualizar_historial_usuario(nombre_usuario, nuevo_historial):
    doc_ref = firestore_db.collection('historial_usuarios').document(nombre_usuario)
    doc_ref.set({'historial': nuevo_historial})

def leer_historial_usuario(nombre_usuario):
    doc_ref = firestore_db.collection('historial_usuarios').document(nombre_usuario)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('historial', [])
    else:
        return []

def actualizar_historial_realtime(nuevo_historial):
    ref = realtime_db.child('historial')
    ref.set(nuevo_historial)

def leer_historial_realtime():
    ref = realtime_db.child('historial')
    return ref.get() or []

def eliminar_historial_realtime():
    ref = realtime_db.child('historial')
    ref.delete()
