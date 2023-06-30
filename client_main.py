# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    from server.util import get_ip

    host = get_ip()
    print('Insert Port')
    port = input()
    try:
        port = int(port)
        uvicorn.run("client:client_interface",
                    host=host, port=port, reload=True)

    except:
        uvicorn.run("client:client_interface",
                    host=host, port=9000, reload=True)
