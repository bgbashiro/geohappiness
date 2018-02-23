from threading import Lock
from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import *
from reader import init_api
from random import random
import csv
# import ML modules
import sys
sys.path.append('MLmodules')
from wordcount import *
from predicter import Predicter

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

def init_ml():
    # Let us fire up our ML, shall we?
    # make sentence and label list from csv
    sent_list = []
    lbl_list = []
    # values of boundaries has been determined by manual analysis
    boundaries =[
        0.18,
    #     0.1958,
    #     0.1680,
        0.17
    ]
    def get_lbl(score):

        if x>boundaries[0]:
            return 2
    #     elif x<boundaries[3]:
    #         return 0
        elif x<boundaries[1]:
            return 0
    #     elif x<boundaries[2]:
    #         return 3
        else:
            return 1

    with open('tweets.csv') as fp:
        csv_r = csv.reader(fp)
        for line in csv_r:
            # some lines have sentence instead of score value
            # ignore them
            try:
                x = float(line[2])
                lbl = get_lbl(x)
                lbl_list.append(lbl)
            except:
                continue
            sent_list.append(line[1])
    # make dictionary list
    with open('dictionary.csv') as fp:
        csv_r = csv.reader(fp)
        dictionary = []
        for x in list(csv_r):
            dictionary.append(x[0])

    pred = Predicter()
    pred.init_labeler(dictionary)
    pred.train(sent_list, lbl_list)

    return pred.predict_sentence

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

        classify_tweet = init_ml()

        while True:
            try:
                res = api.request('statuses/filter', {
                    'locations':'-74.32,40.57,-73.71,40.84'
                })
                for twt in res.get_iterator():
                    if(twt["coordinates"]):
                        label = classify_tweet(twt['text'])
                        print(twt['text'] + ' -> '+str(label))
                        lat = twt["coordinates"]["coordinates"][0]
                        long = twt["coordinates"]["coordinates"][1]
<<<<<<< HEAD
                        socketio.emit('tweet',{
=======
                        txt = twt['text']
                        socketio.emit('tweet',{
>>>>>>> 695287e931eaeb4545f9ec42a8373d0341494905
                                    'lat':lat
                                    ,'long':long
                                    ,'score':label
                                    ,'tweetid':txt
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
