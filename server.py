from socket import *
import random

# puerto del server
server_port = 12000
# crear socket por internet (AF_INET) usando TCP (SOCK_STREAM)
server_socket = socket(AF_INET, SOCK_STREAM)
# asociar puerto al socket
server_socket.bind(('', server_port))
# escuchar conexiones (1 cliente maximo a la espera de conexion)
server_socket.listen(1)

print(' -- Server socket listo -- ')

while True:
    # aceptar nueva conexion en tupla tipo (objeto_socket, (ip_cliente, puerto_cliente))
    connection_socket, addr = server_socket.accept()
    
    # enviar mensaje de conexion exitosa e instrucciones
    connection_msg = "  - Conexion al server socket exitosa \n - Adivina un numero entre 1 y 100  \n - Intentos: 5 \n - '0' para terminar "
    connection_socket.send(connection_msg.encode())
        
    rand_num = random.randint(1, 100)
    remaining_attempts = 5

    print(f'NUEVA CONEXION: Ip Cliente: {addr[0]} - Puerto: {addr[1]} - Numero: {rand_num}')
    
    active_game = True
    while active_game and remaining_attempts > 0: 
        try:
            # recibir intento del cliente
            client_response = connection_socket.recv(1024).decode().strip()
            
            if client_response == '0':
                connection_socket.send(" - Conexion terminada por usuario - ".encode())
                active_game = False
                break
            
            try:
                client_number_guess = int(client_response)
                
                if client_number_guess == rand_num:
                    msg = f" - Victoria. Intentos totales: {5 - remaining_attempts + 1}" 
                    connection_socket.send(msg.encode())
                    active_game = False
                else:
                    remaining_attempts -= 1
                    if remaining_attempts == 0:
                        msg = f" - Derrota - El numero era: {rand_num}"
                        connection_socket.send(msg.encode())
                        active_game = False
                    elif client_number_guess < rand_num:
                        msg = f" - El numero es mayor. Intentos restantes: {remaining_attempts}"
                        connection_socket.send(msg.encode())
                    else:
                        msg = f" - El numero es menor. Intentos restantes: {remaining_attempts}"
                        connection_socket.send(msg.encode())
                    
            except ValueError:
                msg = f" - Entrada invalida. Intentos restantes: {remaining_attempts}"
                connection_socket.send(msg.encode())
                
        except Exception as e:
            print(f"Error: {e}")
            active_game = False
    
    # terminar conexion con cliente
    connection_socket.close()
    
    print(f'FIN CONEXION: Ip Cliente: {addr[0]} - Puerto: {addr[1]}')