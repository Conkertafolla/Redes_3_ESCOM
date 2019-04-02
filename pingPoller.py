# coding=utf-8
import subprocess
import sys
from datetime import datetime

# para enviar el correo
 
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Notificaciones usando firebase Cloud Messaging
import argparse
import json
import requests

from oauth2client.service_account import ServiceAccountCredentials

#SMS
from twilio.rest import Client

#Variables del servicio FCM
PROJECT_ID = 'network-6e3b0'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.
  :return: Access token.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'service-account.json', SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token
# [END retrieve_access_token]

def _send_fcm_message(fcm_message):
  # [START use_access_token]
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  # [END use_access_token]
  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)

def _build_common_message(ip):
  date_ping=datetime.now()
  return {
    'message': {
      'topic': 'news',
      'notification': {
        'title': 'Un dispositivo presenta falla',
        'body': 'La ip '+ ip+' no respondio al ping'
      },
      'data':{
          'ip': ip,
          'date': date_ping.strftime("%m/%d/%Y, %H:%M:%S ")
           
      }
    }
  }

subject = "Hubo errores en dispositivos"
body = "Se adjunta el archivo con el reporte de errores"
sender_email = "equipo.redes3.escom@gmail.com"
receiver_email = "javiervbk@gmail.com"
password = "abcdef1357"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
#message["Bcc"] = receiver_email  # Recommended for mass emails



time_log ="PingPoller"+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")+ ".txt"
log_file=open(time_log,'w')
no_error = True

mensajesms=''
with open('ipTest.txt','r') as ips:
    for ip in ips:
        ip=ip.strip()
        res = subprocess.call(['ping','-c','6',ip])
        date_ping=datetime.now()
        print(res)
        if res == 0:
            print("La direccion "+ip+" respondio correctamente en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n"))
            
        else:
            no_error = False
            log_file.write("La direccion "+ip+" no respondió en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S\n"))
            mensajesms="La direccion "+ip+" no respondió en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S\n")
            log_file.write("Después de 6 intentos:\n")
            res = subprocess.call(['ping','-c','4',ip])
            if res == 0:
                log_file.write("\tRespondió correctamente.\n")
            else:
                log_file.write("\tLa direccion "+ip+" no respondió en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S\n"))
                log_file.write("\tDespués de 4 intentos:\n")
                res = subprocess.call(['ping','-c','2',ip])
                if res == 0:
                    log_file.write("\t\tRespondió correctamente\n")
                else:
                    log_file.write("\t\tFalló finalmente después de 10 intentos.\n")
                    mensajesms=mensajesms+"\t\tFalló finalmente después de 10 intentos.\n"
                    #Envia notificacion
                    common_message = _build_common_message(ip)
                    print('FCM request body for message using common notification object:')
                    print(json.dumps(common_message, indent=2))
                    _send_fcm_message(common_message)
log_file.close()

if not no_error:
    #enviar correo
    message.attach(MIMEText(body, "plain"))
    filename = time_log  # In same directory as script

    # Open file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        "attachment; filename=" +filename,
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

    account_sid = "AC8e9b6afd18749b12132ab968ef48e0ff"
    auth_token  = "8fa253e1e1efc70fe9d092bfbb19261b"

    client = Client(account_sid, auth_token)

    messagesms = client.messages.create(
      to="+525541854182", 
      from_="+12028462580",
      body=mensajesms)
    print(messagesms.sid)
    print ("SMS enviada")
else:
    #nada
    1+3