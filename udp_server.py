import socket, sys
from threading import Thread

HOST = '127.0.0.1' # endereço IP
PORT = 8008        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024 # tamanho do buffer para recepção dos dados
END_TRANSMISSION_FLAG = 'Transmissão finalizada!'
CONFIRMATION_MESSAGE = 'ok'

def getFilePath(receivedText):
    if (receivedText == '1'):
        return 'files/small.txt'
    elif (receivedText == '2'):
        return 'files/medium.txt'
    elif (receivedText == '3'):
        return 'files/large.txt'
    else:
        return

def listenToClient(UDPServerSocket):
    while(True):
        data = UDPServerSocket.recvfrom(BUFFER_SIZE)

        receivedText = data[0].decode('utf-8')
        clientAddress = data[1]

        filePath = getFilePath(receivedText)

        print("Iniciando transmissão de arquivo...")

        # abre o arquivo para leitura
        with open(filePath, 'r') as file:

            # loop para enviar cada linha do arquivo
            for line in file:
                print("\nenviando a linha: " + line)
                UDPServerSocket.sendto(line.encode(), clientAddress)

                print("aguardando confirmação de recebimento...")
                confirmationData = UDPServerSocket.recvfrom(BUFFER_SIZE)

                confirmationText = confirmationData[0].decode('utf-8')

                if (confirmationText != CONFIRMATION_MESSAGE):
                    print("Erro ao enviar a linha: " + line)
                    break

                print("confirmação recebida!")

        file.close()

        print("\n" + END_TRANSMISSION_FLAG)

        UDPServerSocket.sendto(END_TRANSMISSION_FLAG.encode(), clientAddress)

def main(argv):
    try:
        # Create a datagram socket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        UDPServerSocket.bind((HOST, PORT))
        print('Servidor iniciado!\n')
        # Listen for incoming datagrams
        listenToClient(UDPServerSocket)

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             

if __name__ == "__main__":   
    main(sys.argv[1:])