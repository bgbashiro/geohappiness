import React, { Component } from 'react';
import Map from './Map.js';
import './App.css';

const sampleData = {
  "data": [
    {
      "x"    : -10,
      "y"    : 20,
      "score": 0.3
    }
    ,{
      "x"    : 3,
      "y"    : 5,
      "score": 0.8
    },
    {
      "x"    : -10,
      "y"    : 24,
      "score": 0.5
    },
    {
      "x"    : 1,
      "y"    : 2,
      "score": 0.1
    },
    {
      "x"    : -8,
      "y"    : -4,
      "score": 0.92
    },

    {
      "x"    : -2,
      "y"    : 17,
      "score": 0.3
    }
    ,{
      "x"    : 10,
      "y"    : -15,
      "score": 0.8
    },
    {
      "x"    : -10,
      "y"    : -3,
      "score": 0.5
    },
    {
      "x"    : -3,
      "y"    : 15,
      "score": 0.1
    },
    {
      "x"    : -9,
      "y"    : -3,
      "score": 0.92
    }
  ]
}

class App extends Component {
  constructor(props){
    super(props);

    this.state = {}

    this.getData     = this.getData.bind(this);
  }

  componentWillMount(){
    this.getData();
  }

  //Make a fetch request from the API
  getData(){
    let newData = sampleData;

    if(newData !== this.state.data){
      this.setState({
        data: newData
      })
    }
  }

  getEmoji(score){
    switch(true) {
      case (score > 0.8):
        return <span role="img" aria-label="very happy">😄</span>;
      case (score <= 0.8 && score > 0.6):
        return <span role="img" aria-label="happy">😊</span>;
      case (score <= 0.6 && score > 0.4):
        return <span role="img" aria-label="mild">😑</span>;
      case (score <= 0.4 && score > 0.2):
        return <span role="img" aria-label="sad">😞</span>;
      default:
        return <span role="img" aria-label="very sad">😢</span>;
    }
  }

  render() {
    console.log(this.state.data?true:false)

    return (
      <div className="App">
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
        <div className="body">
          {this.state.data?
            this.state.data.data.map((dataPoint) => {
              return (<div key={dataPoint.x * dataPoint.y} className="dataPoint" style={{
                  "left":dataPoint.x + "vw",
                  "top":(50 + dataPoint.y) + "vh"
                }}>
                  {this.getEmoji(dataPoint.score)}
                </div>)
            })
            :null},
          <Map />
        </div>
      </div>
    );
  }
}

export default App;
