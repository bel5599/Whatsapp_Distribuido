from function_db import*





if __name__ == '__main__':
    create_database()
    add_user('Ale','1234')
    add_user('Fernanda','1234')
    add_messenger('Fernanda','Ale','Hola')
    add_messenger('Ale','Fernanda','Hola')