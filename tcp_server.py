import socket, sys, time
from threading import Thread

HOST = '127.0.0.1' # endereço IP
PORT = 8008        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024 # tamanho do buffer para recepção dos dados
END_TRANSMISSION_FLAG = 'Transmissão finalizada!'

def getFilePath(receivedText):
    if (receivedText == '1'):
        return 'files/small.txt'
    elif (receivedText == '2'):
        return 'files/medium.txt'
    elif (receivedText == '3'):
        return 'files/large.txt'
    else:
        return

def handleNewClientSocket(TCPClientSocket,addr):
    while True:
        try:
            data = TCPClientSocket.recv(BUFFER_SIZE)

            if not data:
                break

            receivedText = data.decode('utf-8') # converte os bytes em string

            filePath = getFilePath(receivedText)

            print("Iniciando transmissão de arquivo...")

            # abre o arquivo para leitura
            with open(filePath, 'r') as file:

                # loop para enviar cada linha do arquivo
                for line in file:
                    print("\nenviando a linha: " + line)
                    TCPClientSocket.send(line.encode())
                    time.sleep(0.0000000000001)

            file.close()

            print("\n" + END_TRANSMISSION_FLAG)

            TCPClientSocket.send(END_TRANSMISSION_FLAG.encode())
        except Exception as error:
            print("Erro na conexão com o cliente!!")
            print(error)
            return


def main(argv):
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
            TCPServerSocket.bind((HOST, PORT))
            print('Servidor iniciado. Aguardando conexões...')
            while True:
                TCPServerSocket.listen()
                TCPClientSocket, addr = TCPServerSocket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=handleNewClientSocket, args=(TCPClientSocket,addr))
                t.start()   
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])