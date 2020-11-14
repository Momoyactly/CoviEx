import requests, os, jwt, xmltodict

from app.models import User
from app import GuestUser, Agenda
from datetime import datetime
from app import db  
from secrets import token_urlsafe
import jwt 
import base64
import time,calendar

from dotenv import load_dotenv
load_dotenv()


def sendWebexMsg(texto,roomId=os.environ["idRoomYo"]):
    payload = {"text": str(texto),"roomId": roomId   }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ os.environ["botToken"]
    }
    requests.post( os.environ["urlWebextTeams"], headers=headers, json = payload )

def ourloggin(texto,mandarWebexMsg=False):
    print(texto)
    if mandarWebexMsg:
        sendWebexMsg(texto,os.environ["idRoomTodos"])

def setSchedulingPermissions(host=os.environ["host"]):
    with open("app/setUser.xml") as file: 
        data = file.read()
    url = "https://api.webex.com/WBXService/XMLService"
    payload = data.format(os.environ["webExID"],os.environ["XMLpassword"],os.environ["siteName"],host)
    print(payload)
    headers = {'Content-Type': 'text/plain'}
    response = requests.post( url, headers=headers, data = payload).text
    response = xmltodict.parse(response)
    exitoso = response["serv:message"]["serv:header"]["serv:response"]["serv:result"]
    return exitoso == "SUCCESS"


def createWebexMeeting(nombre,fecha,host=os.environ["host"]):
    with open("app/createMeetings.xml") as file: 
        data = file.read()
    url = "https://api.webex.com/WBXService/XMLService"
    payload = data.format(os.environ["webExID"],os.environ["XMLpassword"],os.environ["siteName"],nombre,fecha,host)
    print(payload)
    headers = {'Content-Type': 'text/plain'}
    response = requests.post( url, headers=headers, data = payload).text
    response = xmltodict.parse(response)
    resultado = str(response["serv:message"]["serv:header"]["serv:response"]["serv:result"])
    if resultado == "SUCCESS":
        ourloggin(resultado+" al crear se sesion de Webex meetings",True)
        meetingKey = response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:meetingkey"]
        with open("app/getmeeting.xml") as file: 
            data = file.read()
        payload = data.format(os.environ["webExID"],os.environ["XMLpassword"],os.environ["siteName"],meetingKey)
        response = requests.post( url, headers=headers, data = payload).text
        response = xmltodict.parse(response)
        sipURL = str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:sipURL"])
        print("EL evento '"+nombre+"' con fecha "+fecha+" ha sido creado exitosamente!!\nCon la SipURL: "+ sipURL)
        return sipURL
    else:
        ourloggin(resultado+" al crear se sesion de Webex meetings",True)
        razon = str(response["serv:message"]["serv:header"]["serv:response"]["serv:reason"])
        ourloggin("La razon es: "+razon,True)

def hostJoined(meetingKey):
    with open("app/getmeeting.xml") as file: 
            data = file.read()
    payload = data.format(os.environ["webExID"],os.environ["XMLpassword"],os.environ["siteName"],meetingKey)
    url = "https://api.webex.com/WBXService/XMLService"
    headers = { 'Content-Type': 'text/plain'}
    response = requests.post( url, headers=headers, data = payload).text
    response = xmltodict.parse(response)
    #print(response)
    hostJoined = str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:hostJoined"])
    return hostJoined == "true"

def webexURL(meetingKey):
    with open("app/getmeeting.xml") as file: 
            data = file.read()
    payload = data.format(os.environ["webExID"],os.environ["XMLpassword"],os.environ["siteName"],meetingKey)
    url = "https://api.webex.com/WBXService/XMLService"
    headers = { 'Content-Type': 'text/plain'}
    response = requests.post( url, headers=headers, data = payload).text
    response = xmltodict.parse(response)
    #print(response)
    return str(response["serv:message"]["serv:body"]["serv:bodyContent"]["meet:meetingLink"])
     

def createJWT(expirationTime,token):
    secret  = os.environ["secret"]
    user_id = os.environ["user_id"]
    key64 = base64.b64decode(secret)
    payload = {
    "sub": token,
    "name": token,
    "iss": user_id,
    "exp": expirationTime
    }
    headers= { "alg": "HS256","typ": "JWT" }
    encoded = str(jwt.encode(payload, key64, algorithm ='HS256', headers=headers).decode("utf-8"))
    return encoded

def sendAgendaSMS(contactos=["5580663521"],fecha="fecha en pruebas",tipo="tipo de prueba"):
    texto = "Se ha agendado una video llamada de "+tipo+"con el INER, con fecha/hora "+str(fecha)+". Recibira por SMS el acceso 10 minutos antes de la fecha/hora programada. Se recomienda ampliamente conectarse a traves de una red tipo WiFi"
    for contacto in contactos:
        sendSMS("+52"+contacto,texto)

def sendWidgetSMS(contacto,token):
    texto = "Servicio de TeleConsulta INER. Para iniciar la videollamada favor de ingresar a la siguiente direccion: {}/widget?token={}".format(os.environ["URLApp"],token) 
    sendSMS("+52"+contacto,texto)

def sendSMS(contacto,text):

    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(os.environ["smsAccount"])
    payload = 'To={}&From={}&Body={}'.format(contacto,os.environ["fromNumber"],text)
    headers = {
    'Authorization': 'Basic '+ os.environ["smsBasicAuth"],
    'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post( url, headers=headers, data = payload).json()
    print(response)
    url = "https://api.twilio.com"+ response["uri"]
    time.sleep(2)
    response = requests.get( url, headers=headers).json()

    texto = "El mensaje: '{}' \nCon status de '{}' al numero {}".format(response["body"],response["status"],response["to"])
    ourloggin(texto,True)



def generarWebex(listaNumeros=["5580663521"],correo=os.environ["host"],nombre="teleconsulta"):
    fecha=datetime.utcnow().timestamp()
    sendWebexMsg(datetime.fromtimestamp(int(fecha)-18000))
    timeForWebex = datetime.utcfromtimestamp(int(fecha)-18000).strftime("%m/%d/20%y %H:%M:00")
    actualTimePlusHR = str(datetime.utcnow().timestamp()+3600)
    sipURL = createWebexMeeting(nombre,timeForWebex,correo)  
    if sipURL is None: return  False
    for numero in listaNumeros:
        token = token_urlsafe(10)[:10]
        guestUser = GuestUser(token = token, expirationTime = actualTimePlusHR,SIP = sipURL)
        db.session.add(guestUser)
        db.session.commit()
        sendWidgetSMS(numero,token)
    return True

def agendarWebex(listaNumeros=["5580663521"],correo=os.environ["host"],nombre="teleconsulta",fecha=datetime.utcnow().timestamp()):
    sendWebexMsg(datetime.utcfromtimestamp(int(fecha)))
    timeForWebex = datetime.utcfromtimestamp(int(fecha)).strftime("%m/%d/20%y %H:%M:00")
    return  createWebexMeeting(nombre,timeForWebex,host=correo)    

def cronSMS(minutos=10):
    actualTimePlusHR = str(datetime.utcnow().timestamp()+3600)
    JSONeventos ={"eventos":[]}
    enXsec = 18000-(60*minutos)
    ahora, enXmin = (datetime.utcnow().timestamp()-18000,datetime.utcnow().timestamp()-enXsec)
    print(ahora,enXmin)
    eventos = db.session.query(Agenda).filter(Agenda.fecha_hora.between(ahora,enXmin)).all()
    for evento in eventos:
        listaNumeros = evento.celulares.split(",")
        JSONevento={"fecha":str(datetime.fromtimestamp(int(evento.fecha_hora))),"numeros":listaNumeros}
        JSONeventos["eventos"].append(JSONevento)
        sipURL = evento.SIP   
        for numero in listaNumeros:
            print(numero)
            token = token_urlsafe(10)[:10]
            guestUser = GuestUser(token = token, expirationTime = actualTimePlusHR,SIP = sipURL)
            db.session.add(guestUser)
            db.session.commit()
            sendWidgetSMS(numero,token)
    return str(JSONeventos)

def existeWebex(correo=os.environ["host"]):
    print(correo)
    return  setSchedulingPermissions(correo)



if __name__ == "__main__":
    sendSMS("+525580663521","texto de prueba")
    sendWebexMsg("prueba")
