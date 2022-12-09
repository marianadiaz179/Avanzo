
from pymongo import MongoClient
from django.conf import settings
import pika


def analisisCredito():
    rabbit_host = '10.128.0.3'
    rabbit_user = 'monitoring_user'
    rabbit_password = 'isis2503'
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    clientes = db['clientes']

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host, 
            credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))

    channel = connection.channel()

    channel.queue_declare(queue='creditos')
    doc1 = 'Mario Castillo;2100000;1000612379;Apple;35;01/01/2022'
    data1 = {'nombre': 'Mario Castillo' , 'salario' : '2100000', 'cedula': '1000612379', 
             'empresa': 'Apple', 'edad' :'35', 'fechaContarto': '01/01/2022', 'estado': 'pendiente'}
    clientes.insert(data1)
    cliente1 = clientes.find({'cedula': '1000612379'})
    print("Se ha agregado el cliente : ")
    print(cliente1)
    
    doc2 = 'Laura Torres;5400000;1000185263;Facebook;31;02/09/2021'
    data2 = {'nombre': 'Laura Torres' , 'salario' : '5400000', 'cedula': '1000185263', 
             'empresa': 'Facebook', 'edad' :'31', 'fechaContarto': '02/09/2021', 'estado': 'pendiente'}
    clientes.insert(data2)
    cliente2 = clientes.find({'cedula': '1000185263'})
    print("Se ha agregado el cliente : ")
    print(cliente2)
    
    infoDocumentos=[doc1,doc2]

    print('Mandando información de los documentos de los clientes. To exit press CTRL+C')

    for i in infoDocumentos:
        channel.basic_publish(exchange='', routing_key='creditos', body=i)
        print("Se ha enviado la información de los documentos "+ i)

    connection.close()

analisisCredito()