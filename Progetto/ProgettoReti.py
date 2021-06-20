# -*- coding: utf-8 -*-
"""
Studente: Zanzi Alessandro
Mail istituzionale: alessandro.zanzi2@studio.unibo.it
Matricola: 0000

Traccia 2, Python Web Server
Consegna:
Si immagini di dover realizzare un Web Server in Python per una azienda ospedaliera.
I requisiti del Web Server sono i seguenti:
- Il web server deve consentire l’accesso a più utenti in contemporanea
- La pagina iniziale deve consentire di visualizzare la lista dei servizi erogati dall’azienda ospedaliera e per 
ogni servizio avere un link di riferimento ad una pagina dedicata.
- L’interruzione da tastiera (o da console) dell’esecuzione del web server deve essere opportunamente 
gestita in modo da liberare la risorsa socket.
- Nella pagina principale dovrà anche essere presente un link per il download di un file pdf da parte del 
browser
- Come requisito facoltativo si chiede di autenticare gli utenti nella fase iniziale della connessione.
"""

import signal
import sys
import http.server
import socketserver

host=''

# Legge il numero della porta dalla riga di comando, di default usa la porta 8080.
if sys.argv[1:]:
  serverPport = int(sys.argv[1])
else:
  serverPort = 8080

# server che consente la connessione di più utenti tramite la gestione di thread. Quando un  
# nuovo utente si collega al server è il metodo SimpleHTTPRequestHandler che si occupa di gestire 
# il multithreading e consegna la pagina richiesta al client.
server = socketserver.ThreadingTCPServer((host, serverPort), http.server.SimpleHTTPRequestHandler)

# funzione che consente l'uscita dal processo tramite Ctrl+C
def close_signal_handler(signal, frame):
    print('Exiting http server (Ctrl+C pressed)')
    try:
        if ( server ):
            server.server_close()
    finally:
        sys.exit(0)
        
def main():
    # Assicura che da tastiera usando la combinazione
    # di tasti Ctrl+C termini in modo pulito tutti i thread generati
    server.daemon_threads = True
    # il Server acconsente al riutilizzo del socket anche se ancora non è stato
    # rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True 
    # interrompe l’esecuzione se da tastiera viene premuto (Ctrl+C)
    signal.signal(signal.SIGINT, close_signal_handler)

    # loop infinito
    try:
        while True:
            server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()

if __name__ == "__main__":
    main() 