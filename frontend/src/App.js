import React, { Component } from 'react';
import Map from './Map.js';
import './App.css';
import { getTweets } from './api';
import TweetBox from './TweetBox';

// const sampleData = {
//   "points": [
//     {
//       "lat"    : 55.9533,
//       "long"   : -3.1883 ,
//       "score"  : 0.3,
//       "tweetid": "Young people have helped lead all our great movements. How inspiring to see it again in so many smart, fearless students standing up for their right to be safe; marching and organizing to remake the world as it should be. We've been waiting for you. And we've got your backs."
//     }
//     ,{
//       "lat"    : 55.9633,
//       "long"   : -3.1783 ,
//       "score"  : 0.8,
//       "tweetid": "ShapeShift (2% of Bitcoin Network) is Now Batching Transactions https://shar.es/1LXkDp  #bitcoin @shapeshift_io"
//     },
//     {
//       "lat"    : 55.9433,
//       "long"   : -3.1983 ,
//       "score"  : 0.5,
//       "tweetid": "Kylie Jenner wiped out $1.3 billion of Snap's market value in one tweet https://bloom.bg/2EKNmCf"
//     },
//     {
//       "lat"    : -74.189623,
//       "long"   : 40.721813,
//       "score"  : 0.1,
//       "tweetid": "Billy Graham was a humble servant who prayed for so many - and who, with wisdom and grace, gave hope and guidance to generations of Americans."
//     }
//   ]
// }

class App extends Component {
  constructor(props){
    super(props);

    this.state = {
      points: []//sampleData.points
    }
  }

  componentWillMount(){
    this.getData();
  }

  //Make a fetch request from the API
  getData(){
    let newData = this.state.points;

    getTweets((err, data) => {
      console.log("New data added! Length: ", newData.length);
      if(!err){
        newData.push(data);
        if(newData.length > 30){
          newData.shift();
        }

        this.setState({
          points: newData
        })
      }
    })
  }


  render() {
    return (
      <div className="App">
        <div className="box App-about">
          <h1 className="App-title">GeoHappiness</h1>
          <p>A map of the happiness of a given city using machine learning to analyse tweet sentiments</p>
          <a href="https://github.com/bashir4909/geohappiness">about the project</a>
        </div>
        <div className="box App-legend">
          <p>
            <span role="img" aria-label="very happy">😄</span> - Very Happy<br/>
            {/* <span role="img" aria-label="happy">😊</span> - Happy<br/> */}
            <span role="img" aria-label="mild">😑</span> - Mild<br/>
            {/* <span role="img" aria-label="sad">😞</span> - Sad<br/> */}
            <span role="img" aria-label="very sad">😢</span> - Very Sad
          </p>
        </div>
        <Map
          points={this.state.points}
          googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyAVUv_3RF42tNv2FAsg2tukrSMf2Ns5J7Q&v=3.exp&libraries=geometry,drawing,places"
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `100vh` }} />}
          mapElement={<div style={{ height: `100%` }} />}
        />
        <div className="box App-tweets">
          {JSON.stringify(this.state.points) !== "[]"?
            this.state.points.map((dataPoint) => {
              if(dataPoint.tweetid){
                return <TweetBox key={dataPoint.score} text={dataPoint.tweetid}/>
              } else {
                return null;
              }
            }):<div style={{marginTop: "50%", color: "gray"}}>"Twitter Feed"</div>
          }
        </div>
      </div>
    );
  }
}

export default App;
