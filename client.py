from socket import *

try:
    # ip server
    server_address = '200.13.4.198'  
    # puerto server
    server_port = 12000        

    # crear socket por internet (AF_INET) usando UDP (SOCK_STREAM)
    client_socket = socket(AF_INET, SOCK_STREAM)

    # conectar al servidor
    client_socket.connect((server_address, server_port))
    print("-Iniciando conexion-")

    # recibir respuesta de conexion 
    connection_msg = client_socket.recv(1024).decode()
    print(connection_msg)

    active_game = True
    while active_game:
        attemp = input("-Tu intento: ").strip()

        if attemp == '':
            print('-Debe ingresar algo')
            continue
        
        # enviar datos al servidor 
        client_socket.send(attemp.encode())
        
        # recibir respuesta del servidor 
        server_response = client_socket.recv(1024).decode()
        print(f"-Respuesta server:\n{server_response}")
        
        if  'Conexion' in server_response or 'Derrota' in server_response or 'Victoria' in server_response:
            active_game = False

    # cerrar el socket
    client_socket.close()
    print("-Conexion con server socket terminada")

except Exception as e:
    print(f"Error: {e}")