import openSocket from 'socket.io-client';

const  socket = openSocket('http://127.0.0.1:5000/');


function getTweets(callBack) {
  socket.on('tweet', (data) => {
    callBack(null, data)
  });

  // socket.emit('subscribeToTimer', 1000);
}

export { getTweets };
