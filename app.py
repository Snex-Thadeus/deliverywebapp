from deliverywebapp import app
import eventlet.wsgi


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(port=9001)
    #eventlet.wsgi.server(eventlet.listen(('', 9001)), app)


