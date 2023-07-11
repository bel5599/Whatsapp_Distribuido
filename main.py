from data.database_client import DataBaseClient
from data.database_entity import DataBaseUser
from client.client_node import ClientNode


# def f(data1:DataBaseClient):
#     data1.add_contacts('Daniela','Ale',"el bobo")

if __name__ == '__main__':
    
    #database = DataBaseClient("base de datos")


    cliente = ClientNode()

    cliente.login_user('bel', '1234', [])

    cliente.add_contacts("nick", "nick2")
    cliente.add_contacts("albert", "albert2")
    cliente.add_contacts("ferdi", "ferdi2")
    cliente.add_contacts("alonso", "alonso2")

    # cliente.add_messenges("nick", "alonso", "feo")
    # cliente.add_messenges("nick", "ferdi", "loco")
    # cliente.add_messenges("alonso", "albert", "bonito")
    
    # cliente.add_messenges('bel','nick','probando')
    
    # cliente.delete_chat("nick", "alonso")
    # cliente.delete_chat("nick", "ferdi")
    # cliente.delete_chat("alonso", "albert")
    
    # cliente.search_chat('alonso','albert')
    # for c in cliente.search_chat('alonso','albert'):
    #     print(c)
    
    # chats = cliente.get_chats()
    # for c in chats:
    #     print(c)
        
    # for cont in cliente.get_contacts():
    #     print(cont)
    # # print(cliente.get_contacts())

    # for cont in cliente.get_messages():
    #     print(cont)
    # # print(cliente.get_messages())
