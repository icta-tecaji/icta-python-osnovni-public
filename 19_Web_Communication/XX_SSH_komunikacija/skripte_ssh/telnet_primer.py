import getpass
import telnetlib

def create_dirs(dir_list, path, host, user, password, port=23):
    with telnetlib.Telnet(host, port) as tn:
        print(f"--> connected to host: {host} on port: {port}")
        
        tn.read_until(b"login: ")
        tn.write(user.encode('ascii') + b"\n")

        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        
        print(f"--> succsessful login for user: {user}")
            
        for dir_name in dir_list:
            path_name = f'{path}/{dir_name}'
            command = f'mkdir -v {path_name}\n'
            tn.write(command.encode('ascii'))
            succsess_mesage = f"mkdir: created directory '{path_name}'".encode('ascii')
            res = tn.read_until(succsess_mesage, timeout=2)
            if succsess_mesage in res:
                print(f'--> {dir_name} created successfully')
            else:
                print(f'--> {dir_name} creation failed')

        tn.write(b"exit\n")
        print(tn.read_all().decode('ascii'))


create_dirs(['dir1', 'dir2', 'dir3'], path='/home/testuser/telnet-test', 
                    host='ssh-telnet-test',
                    user='testuser',
                    password='test')