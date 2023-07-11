from data.database_client import DataBaseClient
from data.database_entity import DataBaseUser
from client.client_node import ClientNode


# def f(data1:DataBaseClient):
#     data1.add_contacts('Daniela','Ale',"el bobo")

if __name__ == '__main__':
    
    database = DataBaseClient("base de datos")


    cliente = ClientNode()

    cliente.login_user('bel', '1234', [])

    cliente.add_contacts("nick", "nick2")
    cliente.add_contacts("albert", "albert2")
    cliente.add_contacts("ferdi", "ferdi2")
    cliente.add_contacts("alonso", "alonso2")

    cliente.add_messenges("nick", "alonso", "feo")
    cliente.add_messenges("nick", "ferdi", "loco")
    cliente.add_messenges("alonso", "albert", "bonito")

    for cont in cliente.get_contacts():
        print(cont)
    # print(cliente.get_contacts())

    # for cont in cliente.get_messages():
    #     print(cont)
    # # print(cliente.get_messages())
