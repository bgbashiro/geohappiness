from threading import Lock
from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import *
from reader import init_api
from random import random

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
api = init_api()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

with app.app_context():
    """This is very premature server and very fragile, emits 
    json object like this 
    {
        'lat':some number
        'long':some number
        'score':some number between 0 and 1
    }
    lat long comes from actual realtime tweets, however score is calculated by dummy
    function, will transfer it into ML in near future
    to receive the data use socketio, add this to html
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.5/socket.io.min.js"></script>
        <script>
        namespace = '/test'
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
        </script>
    listening for tweets is like this
    socket.on('tweet', (data) => {
        some stuff here
    });
    where data is JSON object
    """

    # please be careful with this one, can easily fail
    def background_thread():
        """Listens for tweets when it gets tweet with location emits through socket with name 'tweet'"""
        def dummy_classifier(tweet):
            return random()
        while True:
            try:
                res = api.request('statuses/filter', {
                    'locations':'-74.32,40.57,-73.71,40.84'
                })
                for twt in res.get_iterator():
                    if(twt["coordinates"]):
                        print(twt["coordinates"])
                        score = dummy_classifier(twt["text"])
                        lat = twt["coordinates"]["coordinates"][0]
                        long = twt["coordinates"]["coordinates"][1]
                        socketio.emit('tweet',{ 
                                    'lat':lat
                                    ,'long':long
                                    ,'score':score
                                    }, namespace='/test')
            except TwitterRequestError as e:
                if e.status_code < 500:
                    # something needs to be fixed before re-connecting
                    raise
                else:
                    # temporary interruption, re-try request
                    pass
            except TwitterConnectionError:
                # temporary interruption, re-try request
                pass

    
    @app.route('/')
    def index():
        return render_template('index.html', async_mode=socketio.async_mode)


    if __name__ == '__main__':
        socketio.start_background_task(background_thread)
        socketio.run(app, debug=True)
