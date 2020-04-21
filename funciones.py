import requests, os
from dotenv import load_dotenv
load_dotenv()


def sendWebexMsg(texto):
    payload = {"text": texto,"roomId": os.environ["idRoomYo"]}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ os.environ["botToken"]
    }
    requests.post( os.environ["urlWebextTeams"], headers=headers, json = payload)

def getToken():
    return "token"


def sendSMS(directorio):
    for contacto in directorio:
        text = "Servicio de TeleConsulta. Para iniciar la videollamada favor de ingresar a la siguiente direccion: https://4c9366b9.ngrok.io/widget"
        params = {'from': os.environ["sender"], 'text': text, 
                'to': contacto[1], 'api_key': os.environ["api_key"], 
                'api_secret': os.environ["api_secret"]}
        r = requests.post(os.environ["urlSMS"], params=params)
        if r.status_code == 200:
            print (r.json())
        else:
            print(r.status_code)

if __name__ == "__main__":
    directorio =[("Uriel","+5215580663521")]
    sendSMS(directorio)
    sendWebexMsg("prueba")