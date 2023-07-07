#from database import DataBase
from database_client import DataBaseClient
from database_entity import DataBaseUser




if __name__ == '__main__':

    data1 = DataBaseClient('data1')
    #data1.add_user('Ale','1234')
    # data1.add_user('Fernanda','1234')
    #data1.add_messenger('Fernanda','Ale','Hola')
    # data1.add_messenger('Ale','Fernanda','Hola')
    data1.add_contacts('Daniela','Ale',"el bobo")
    data1.add_contacts('Roxana','Ale',"el bobo")
    
    data1.delete_contact('Daniela','Ale')
    #data1.add_contacts('Daniela','Ale',"el bobo")
    #data2 = DataBaseUser('data2')
    #data2.add_user('Ale','1234','12344444','9000')
    # data2.add_user('Roxana','1234')
    # data2.add_messenger('Fernanda','Ale','Hola')
    # data2.add_messenger('Ale','Fernanda','Hola')
    # data2.add_messenger('Ale','Roxana','Hola')
    
    #data1.copy_database(data2)
    #data1.delete_user("Roxana")