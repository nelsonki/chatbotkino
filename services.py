miSorteo=''
# -*- coding: utf-8 -*-
from flask import jsonify
import requests
import sett
import json
import time
import readcsv

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text, premios=None,premio_number=None):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    if premio_number:
        found_prize = next((p for p in premios if p["Premio"] == premio_number), None)
        if found_prize:
            data = json.dumps(
                {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": number,
                    "type": "text",
                    "text": {
                        "body": f"Premio: {found_prize['Premio']}, Descripción: {found_prize['Descripcion']}"
                    }
                }
            )
        else:
            data = json.dumps(
                {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": number,
                    "type": "text",
                    "text": {
                        "body": "Lo siento, no encontramos el premio."
                    }
                }
            )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data


 

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data


def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(1)

    if "hola" in text:
        body = "¡Hola! 👋 Bienvenido al Kino Táchira. ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo Kino Táchira"
        options = ["🔍 consultar sorteo", "📜 descargar resultados", "💰 proximos premios"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)

    elif "consultar sorteo" in text:
        body = "Tenemos varias sorteos en los que puedes consultar. ¿Selecciona un sorteo?"
        footer = "Equipo Kino Táchira"
        options = ["sorteo-42", "sorteo-41"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)

    elif "sorteo-42" in text or "sorteo-41" in text:
        global miSorteo
        miSorteo = text
        print(miSorteo)
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, ahora ingresa el numero del serial:")
        #data = readcsv.read_csv_file(sett.document_premios)
        #print(data)
        #return jsonify(data)
        #miValor=[10,11,12,23,76,45]
        # Convert the miValor list to a string and send it as a message
        #textMessageData = text_Message(number, data)
        enviar_Mensaje_whatsapp(textMessage)
        #enviar_Mensaje_whatsapp(sticker)
        #enviar_Mensaje_whatsapp(textMessage) 

    elif text.isdigit():
        print(miSorteo)
        sticker = sticker_Message(number, get_media_id("anotado", "sticker"))
        data = readcsv.read_csv_file(sett.document_premios, text, miSorteo)
        print(data)
        textMessageData = text_Message(number, data)
        #textMessage = text_Message(number,"", readcsv.read_csv_file(sett.document_premios), text)
        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessageData)
   
    elif "descargar resultados" in text:
        body = "Selecciona"
        footer = "Equipo Kino Táchira"
        options = ["listin nuevo", "listin anterior"]
        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))
        list.append(listReplyData)
        list.append(sticker)

    elif "listin nuevo" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento...")
        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        #time.sleep(1)
        document = document_Message(number, sett.document_url_nuevo, "Listo 👍🏻", "listin")
        enviar_Mensaje_whatsapp(document)
        time.sleep(1)

    elif "listin anterior" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento...")
        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        #time.sleep(1)
        document = document_Message(number, sett.document_url_medio, "Listo 👍🏻", "listin")
        enviar_Mensaje_whatsapp(document)
        time.sleep(1)

    elif "proximos premios" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento...")
        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        #time.sleep(1)
        document = document_Message(number, sett.document_url_prospecto, "Listo 👍🏻", "listin")
        enviar_Mensaje_whatsapp(document)
        time.sleep(1)

    elif "sí, agenda reunión" in text :
        body = "Estupendo. Por favor, selecciona una fecha y hora para la reunión:"
        footer = "Equipo Kino Táchira"
        options = ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]
        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
        
    elif "7 de junio, 2:00 pm" in text:
        body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
        footer = "Equipo Kino Táchira"
        options = ["✅ Sí, por favor", "❌ No, gracias."]
        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
        
    elif "no, gracias." in text:
        textMessage = text_Message(number,"Perfecto! No dudes en contactarnos si tienes más preguntas. ¡Hasta luego! 😊")
        list.append(textMessage)
        
    else:
        body = "Lo siento, no entendí lo que dijiste. ¿Puedes elegir alguna de estas opciones?"
        footer = "Equipo Kino Táchira"
        options = ["🔍 consultar", "💰 listines"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)        
        #data = text_Message(number,"Lo siento, no entendí lo que dijiste. ¿Puedes elegir alguna de estas opciones?")
        #list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)

def replace_start(number): #validar el numero de telefono venezuela, aqui se puede colocar algun otro cambio dependiendo del pais
    if isinstance(number, int):
        number = str(number)
    return number.replace('whatsapp:', '').replace('+', '')
