from API_DB import ApiDB
from API_netmiko import ApiNetmikoGabo

def autenticar(usuario,contraseña):
    return usuario == 'gmedina' and contraseña == 'cisco123'

def main():
    print('JALTECH\nEl acceso no autorizado es ilegal.')
    while True:
        username = input('Usuario: ')
        password = input('Contraseña: ')

        if autenticar(username,password):
            print('Espere mientras se comprueba el estado de los dispositivos.')
            while True:
                #Aqui va la funcion que intenta conectarse a los dispositivos registrados en la base de datos.
                print('''¿Que desea hacer?
                  1.-Registrar un nuevo dispositivo 
                  2.-Configuracion de routers
                  3.-Configuracion de switches
                  4.-Estado de la topologia
                  5.-Backups
                  6.-Generar reporte
                  7.-Salir''')
            
                decision = int(input('R='))

                if decision == 1:#Registrar nuevo dispositivo
                    usuario = input('¿Cual es el usuario del nuevo dispositivo?: ')
                    contraseña = input('¿Cual es la contraseña del usuario?: ')
                    secret = input('¿Cual es la contraseña para el modo privilegiado?: ')
                    host = input('Porfavor proporcione la ip de una interfaz activa del dispositivo: ')
                    netmiko_conn.agregar_dispositivo(host,usuario,contraseña,secret)

                if decision == 2:#Configuracion de routers
                    pass
                if decision == 3:#Configuracion de switches
                    pass 
                if decision == 4:#Estado de la topologia
                    pass                
                if decision == 5:#Backups
                    pass
                if decision == 6:#Generar reporte
                    pass 
                if decision == 7:
                    break
                else:
                    print('\nPorfavor seleccione una opcion valida.')



        else:
            print('Usuario y/o contraseña incorrectos.\n\n')

if __name__ == '__main__':
    db_conn = ApiDB()
    netmiko_conn = ApiNetmikoGabo()
    main()