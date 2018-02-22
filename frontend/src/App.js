import React, { Component } from 'react';
import Map from './Map.js';
import './App.css';
import { getTweets } from './api';

const sampleData = {
  "data": [
    {
      "x"    : 55.9533,
      "y"    : -3.1883 ,
      "score": 0.3
    }
    ,{
      "x"    : 55.9633,
      "y"    : -3.1783 ,
      "score": 0.8
    },
    {
      "x"    : 55.9433,
      "y"    : -3.1983 ,
      "score": 0.5
    },
    {
      "x"    : -74.189623,
      "y"    : 40.721813,
      "score": 0.1
    }
  ]
}

class App extends Component {
  constructor(props){
    super(props);

    this.state = {};

    this.getData = this.getData.bind(this);
  }

  componentWillMount(){
    this.getData();
  }

  //Make a fetch request from the API
  getData(){
    let newData = sampleData;

    getTweets((err, data) => {
      console.log(data);

      if(data){
        newData = data;
      }else {
        newData = sampleData
      }
    })

    console.log(newData);
    if(newData !== this.state.data){
      this.setState({
        data: newData
      })
    }
  }

  render() {
    return (
      <div className="App">
        <Map
          data={this.state.data}
          googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyAVUv_3RF42tNv2FAsg2tukrSMf2Ns5J7Q&v=3.exp&libraries=geometry,drawing,places"
          loadingElement={<div style={{ height: `100%` }} />}
          containerElement={<div style={{ height: `100vh` }} />}
          mapElement={<div style={{ height: `100%` }} />}
        />
        <div className="box App-about">
          <h1 className="App-title">GeoHappiness</h1>
          <p>A map of the happiness of Edinburgh using machine learning to analyse tweet sentiments</p>
          <a href="">about the project</a>
        </div>
        {/* <div className="box App-tweets">
          <TweetBox />
        </div> */}
        <div className="box App-legend">
          <p>
            <span role="img" aria-label="very happy">😄</span> - Very Happy<br/>
            <span role="img" aria-label="happy">😊</span> - Happy<br/>
            <span role="img" aria-label="mild">😑</span> - Mild<br/>
            <span role="img" aria-label="sad">😞</span> - Sad<br/>
            <span role="img" aria-label="very sad">😢</span> - Very Sad
          </p>
        </div>
      </div>
    );
  }
}

export default App;
