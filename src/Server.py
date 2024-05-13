#!/usr/bin/env python3
"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone.
Corso di Programmazione di Reti - Università di Bologna"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from datetime import datetime

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def acceptConnection():
    while True:
        
        try:
            clientSocket, clientAddress = SERVER.accept()
            print("%s:%s si è collegato." % clientAddress)
            #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
            clientSocket.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            # ci serviamo di un dizionario per registrare i client
            addresses[clientSocket] = clientAddress
            #diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=clientHandle, args=(clientSocket,)).start()
        except Exception:
            print("Exception, closing server...")
            break
    for x in clients.keys():
        x.close()
        

"""La funzione seguente gestisce la connessione di un singolo client."""
def clientHandle(clientSocket):  # Prende il socket del client come argomento della funzione.
    try:
        name = clientSocket.recv(BUFSIZ).decode("utf8")
        #da il benvenuto al client e gli indica come fare per uscire dalla chat quando ha terminato
        welcome = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % name
        clientSocket.send(bytes(welcome, "utf8"))
        msg = "%s si è unito all chat!" % name
        #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
        broadcast(bytes(msg, "utf8"))
        #aggiorna il dizionario clients creato all'inizio
        clients[clientSocket] = name
        
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
        while True:
            msg = clientSocket.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                clientSocket.send(bytes("{quit}", "utf8"))
                clientSocket.close()
                del clients[clientSocket]
                broadcast(bytes("%s ha abbandonato la Chat." % name, "utf8"))
                break
            #gestisco l'eccezione che il client si disconnetta in maniera forzata
    except ConnectionResetError:
        adr=addresses.get(clientSocket)
        clientSocket.close()
        #condizione nel caso il client si disconnettesse prima di avere inserito il nome e dunque di non essere inserito nei clienti
        if clientSocket in addresses.keys():
            del addresses[clientSocket]
        if clientSocket in clients.keys():
            del clients[clientSocket]
            broadcast(bytes("%s ha abbandonato la Chat." % name, "utf8"))
        
        print(str(adr)+" disconnessio.")            
            
                
       

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefix=""): # il prefisso è usato per l'identificazione del nome.
    #aggiungo la data in cui è stato inviato il messaggio dal server ai client
    dateString = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msgWithDate=msg+bytes(" ["+dateString+"]","utf8")
    for utente in clients:
        utente.send(bytes(prefix, "utf8")+msgWithDate)

        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    acceptThread = Thread(target=acceptConnection)
    acceptThread.start()
    acceptThread.join()
    SERVER.close()
