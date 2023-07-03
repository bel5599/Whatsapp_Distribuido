# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    from shared import get_ip
    from client.client import client_interface

    host = get_ip()
    print('Insert Port')
    port = input()
    try:
        port = int(port)
        uvicorn.run(client_interface,
                    host=host, port=port)

    except:
        uvicorn.run(client_interface,
                    host=host, port=9000)
