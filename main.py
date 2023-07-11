from data.database_client import DataBaseClient
from data.database_entity import DataBaseUser
from client.client_node import ClientNode
from server.node.entity_node import EntityNode


# def f(data1:DataBaseClient):
#     data1.add_contacts('Daniela','Ale',"el bobo")

if __name__ == '__main__':
    
    #database = DataBaseClient("base de datos")


    # cliente = ClientNode()

    # cliente.login_user('bel', '1234', [])

    #Contacts
    # cliente.add_contacts("nick", "nick2")
    # cliente.add_contacts("albert", "albert2")
    # cliente.add_contacts("ferdi", "ferdi2")
    # cliente.add_contacts("alonso", "alonso2")

    # cliente.add_contacts("piruli", "piruli2")
    # cliente.update_contact("piruli", "paleta")
    # print(cliente.update_contact("new", "new2"))

    # print(cliente.contain_contact("new"))
    # print(cliente.contain_contact("piruli"))

    # print(cliente.delete_contact("new"))
    # print(cliente.delete_contact("nick"))

    # print(cliente.get_name("new"))
    # print(cliente.get_name("piruli"))

    # print(cliente.get_id("new"))
    # print(cliente.get_id())

    #Messages
    # print(cliente.delete_messenges(48))
    # print(cliente.search_messenges_to("nick", 'bel'))
    # print(cliente.search_messenges_to("tw", "nick"))





    
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
    # print(cliente.get_messages())
    entity_node = EntityNode('123.456.789.56', '4321',64)
    entity_node.add_user("bel", "1233", '123.456.789.56', '4321', -1)
    entity_node.add_user("daniela", "2222", '123.456.789.56', '4321', -1)
    entity_node.add_user("edu", "7412", '123.456.789.56', '4321', -1)

    print(entity_node.get_pasword("daniela", -1))

    print(entity_node.delete_user("bel", -1))

    print(entity_node.update_user("bel", '123.456.967.64', '4876', -1))

    print(entity_node.update_user("daniela", '123.456.967.64', '4876', -1))

    print(entity_node.get_ip_port('daniela', -1))

    entity_node.add_user("edu", "7412", '123.456.789.56', '4321', -1)

    # print(entity_node.search_entity_node('edu'))

    # entity_node.add_messages()

    for cont in entity_node.get_users(-1):
        print(cont)
    # print(cliente.get_contacts())

    entity_node.add_messages("nick", "alonso", "feo", -1)
    entity_node.add_messages("nick", "ferdi", "loco", -1)
    entity_node.add_messages("alonso", "albert", "bonito", -1)

    # for cont in entity_node.get(-1):
    #     print(cont)