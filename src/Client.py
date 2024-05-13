#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

"""funzione che segue ha il compito di gestire la ricezione dei messaggi."""
def receive():
    while True:
        try:
            #quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            #arrivano sul socket
            msg = mySocket.recv(BUFSIZ).decode("utf8")
            #visualizziamo l'elenco dei messaggi sullo schermo
            #e facciamo in modo che il cursore sia visibile al termine degli stessi
            msgList.insert(tkt.END, msg)
            # Nel caso di errore e' probabile che il client abbia abbandonato la chat.
        except OSError:  
            break

"""funzione che segue gestisce l'invio dei messaggi."""
def send(event=None):
    
    try:
        # prende il valore dalla message box
        msg = msgVar.get()
        # libera la message box
        msgVar.set("")
        # invia il messaggio sul socket
        mySocket.send(bytes(msg, "utf8"))
        #se viene inviato il messaggio che server per uscire dalla chat {quit} chiudo il socket e la finestra
        if msg == "{quit}":
            mySocket.close()
            window.quit()
            #gestisco l'eccezione nel caso il server viene chiuso forzatamente
    except ConnectionResetError:
        print("in server si è chiuso forzatamente")
        mySocket.close()
        window.quit()
    

"""funzione che segue viene invocata quando viene chiusa la finestra della chat."""
def on_closing(event=None):
    msgVar.set("{quit}")
    send()
"""Funzione per pulire la chat"""
def clearChat():
    msgList.delete(0,'end')


"""Creo la mia GUI utilizzando la libreria Tkinter"""
window = tkt.Tk()
window.title("CHAT ROOM")

#creiamo il Frame per contenere i messaggi
msgFrame = tkt.Frame(window)
#creiamo una variabile di tipo stringa per i messaggi da inviare.
msgVar = tkt.StringVar()
#creiamo una scrollbar per navigare tra i messaggi precedenti.
msgScrollbar = tkt.Scrollbar(msgFrame)

# La parte seguente contiene i messaggi.
msgList = tkt.Listbox(msgFrame, height=15, width=50, yscrollcommand=msgScrollbar.set)
msgScrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msgList.pack(side=tkt.LEFT, fill=tkt.BOTH)
msgList.pack()
msgFrame.pack()

#Creiamo il campo di input e lo associamo alla variabile stringa
msgBox = tkt.Entry(window, textvariable=msgVar)
# leghiamo la funzione send al tasto Return
msgBox.bind("<Return>", send)

msgBox.pack()
#creiamo il tasto invio e lo associamo alla funzione send
msgSendButton = tkt.Button(window, text="Invio", command=send)
#bottone per il clear
msgClearButton = tkt.Button(window, text="Pulisci", command=clearChat)
#bottone per uscire (alternativo allo scrivere {quit} o chiudere con la x)
msgQuitButton = tkt.Button(window, text="Quit", command=on_closing)
#integriamo il tasto nel pacchetto
msgSendButton.pack()
msgQuitButton.pack()
msgClearButton.pack()
window.protocol("WM_DELETE_WINDOW", on_closing)

#----Connessione al Server----
HOST = '127.0.0.1'
PORT = 53000

BUFSIZ = 1024
ADDR = (HOST, PORT)

mySocket = socket(AF_INET, SOCK_STREAM)
try:
    mySocket.connect(ADDR)
    receiveThread = Thread(target=receive)
    receiveThread.start()
    # Avvia l'esecuzione della Finestra Chat.
    tkt.mainloop()
except ConnectionRefusedError:
    print("Server non in linea, impossibile stabilire la connessione")
    mySocket.close()

