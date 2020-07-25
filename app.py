from deliverywebapp import app
import eventlet
import eventlet.wsgi


if __name__ == '__main__':
    # app.run(port=9001)
    eventlet.wsgi.server(eventlet.listen(('', 9001)), app)


