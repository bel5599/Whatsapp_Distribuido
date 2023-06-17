from function_db import*





if __name__ == '__main__':
    create_database()
    add_user('Ale')
    add_user('Fernanda')
    add_messenger('Fernanda','Ale','Hola')
    add_messenger('Ale','Fernanda','Hola')