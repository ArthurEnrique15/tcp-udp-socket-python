import socket, sys
import time

HOST = '127.0.0.1'  # endereço IP
PORT = 8008         # Porta utilizada pelo servidor
BUFFER_SIZE = 20000  # tamanho do buffer para recepção dos dados
END_TRANSMISSION_FLAG = 'Transmissão finalizada!'

def getReceivedFilePath(fileSize):
    if (fileSize == '1'):
        return 'files/small_received.txt'
    elif (fileSize == '2'):
        return 'files/medium_received.txt'
    elif (fileSize == '3'):
        return 'files/large_received.txt'
    else:
        return

def getFileSizeFromInput():
    print("\nSelecione o tamanho do arquivo:")
    print("1. small")
    print("2. medium")
    print("3. large\n")

    fileSize = input("Digite o número da opção desejada: ")

    while (fileSize not in ['1', '2', '3']):
        print("\nOpção inválida!\n")

        print("Selecione o tamanho do arquivo:")
        print("1. small")
        print("2. medium")
        print("3. large\n")

        fileSize = input("Digite o número da opção desejada: ")

    return fileSize

def receiveFile(TCPClientSocket):
    fileSize = getFileSizeFromInput()

    TCPClientSocket.send(fileSize.encode())

    filePath = getReceivedFilePath(fileSize)

    file = open(filePath, "w")

    startTime = time.time()

    # loop para receber cada linha do arquivo
    while True:
        # recebe a linha
        data = TCPClientSocket.recv(BUFFER_SIZE)

        receivedText = data.decode('utf-8')

        print("texto recebido: " + receivedText)

        receivedEndFlag = False

        # se recebeu a flag, remove ela da string
        if (END_TRANSMISSION_FLAG in receivedText):
            receivedText = receivedText.replace(END_TRANSMISSION_FLAG, '')
            receivedEndFlag = True

        file.write(receivedText)

        # se recebeu a flag, finaliza o loop
        if (receivedEndFlag):
            break

    endTime = time.time()

    elapsedTimeInSeconds = endTime - startTime

    file.close()

    print("\nArquivo recebido!")
    print("Tempo gasto na transferência: {:.2f} segundos".format(elapsedTimeInSeconds))
    

def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
            TCPClientSocket.connect((HOST, PORT))
            print("Conectado ao servidor!")

            while(True):
                print("\nSelecione o que deseja fazer:")
                print("1. Receber um arquivo do servidor")
                print("2. Encerrar o programa\n")

                option = input("Digite o número da opção desejada: ")
                
                if (option == '1'):
                    receiveFile(TCPClientSocket)
                    continue
                    
                elif (option == '2'):
                    print('\nFechando a conexão com o servidor!')
                    TCPClientSocket.close()
                    print('Encerrando o programa!')
                    return
                else:
                    print("\nOpção inválida!\n")
                    continue
                    
    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return

if __name__ == "__main__":   
    main(sys.argv[1:])

