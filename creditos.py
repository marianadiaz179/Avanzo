from pymongo import MongoClient
import pika
from sys import path
from os import environ
import django
from datetime import datetime
import time
MONGO_CLIENT="mongodb://monitoring_user:isis2503@10.128.0.6:27017"

path.append('monitoring/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')
django.setup()

from creditos.services.services_creditos import send_email


def main(queue='creditos'):
  rabbit_host = '10.128.0.3'
  rabbit_user = 'monitoring_user'
  rabbit_password = 'isis2503'
  client = MongoClient(MONGO_CLIENT)
  db = client.monitoring_db
  clientes = db['clientes']

  connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
  channel = connection.channel()
  channel.queue_declare(queue=queue)
  
  def callback(ch, method, properties, body):
    inicial = time.time()
    documentos = body.decode()
    respuesta = "Rechazado"
    documentos = documentos.split(";")
    clientes.update_many({'cedula':documentos[2]},{ "$set": {'estado': 'Rechazado'}})
    fecha_mes = (datetime.strptime(documentos[5], '%d/%m/%Y')).month not in range(9,11)

    if documentos[3] == "Apple":
      if int(documentos[1]) >= 2000000:
        if int(documentos[4]) >= 30:
          if fecha_mes == True:
            respuesta = "Aprobado"
            clientes.update_many({'cedula':documentos[2]},{ "$set": {'estado': 'Aprobado'}})
            

    elif documentos[3] == "Facebook":
      if int(documentos[1]) >= 3000000:
        if int(documentos[4]) >= 30:
          if fecha_mes == True:
            respuesta = "Aprobado"
            clientes.update_many({'cedula':documentos[2]},{ "$set": {'estado': 'Aprobado'}})

    elif documentos[3] == "Microsoft":
      if int(documentos[1]) >= 7000000:
        if int(documentos[4]) >= 30:
          if fecha_mes == True:
            respuesta = "Aprobado"
            clientes.update_many({'cedula':documentos[2]},{ "$set": {'estado': 'Aprobado'}})
            
    cliente = clientes.find({'cedula': documentos[2]})
    for dto in cliente:
          infoCliente = 'nombre: ' + dto['nombre'] + ", " + 'cedula: ' + dto['cedula'] + ", empresa: " 
          + dto['empresa'] + ", estado: " + dto['estado']

    time.sleep(3)
    print("El credito de " + cliente['nombre'] + " ha sido: " + respuesta)
    print("Se ha actualizado el estado del cliente")
    print(infoCliente)
    #send_email(respuesta)
    print("-----------------")
    
    final = time.time()
    print("El tiempo de ejecución fue: " + str(final-inicial))

  channel.basic_consume(queue='creditos', on_message_callback=callback, auto_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  


if __name__ == '__main__':
    main(queue='creditos')
