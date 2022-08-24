from src import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='192.168.10.60', port='5000', debug=True)
    # app.run(host='localhost', port='5000', debug=True)