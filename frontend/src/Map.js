import React from 'react';
import { GoogleMap, withGoogleMap, withScriptjs, OverlayView } from 'react-google-maps';
import MapStyles from './MapStyles.json';

class Map extends React.Component {
  constructor(props){
    super(props);

    this.state = props;

    this.handleEmojiClick = this.handleEmojiClick.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if(JSON.stringify(this.state.points) !== JSON.stringify(nextProps.points)) // Check if it's a new user, you can also use some unique, like the ID
    {
      this.setState(nextProps);
    }
  }


  getEmoji(score){
    switch(true) {
      case (score > 0.8):
        return <span className="emoji" role="img" aria-label="very happy">😄</span>;
      case (score <= 0.8 && score > 0.6):
        return <span className="emoji" role="img" aria-label="happy">😊</span>;
      case (score <= 0.6 && score > 0.4):
        return <span className="emoji" role="img" aria-label="mild">😑</span>;
      case (score <= 0.4 && score > 0.2):
        return <span className="emoji" role="img" aria-label="sad">😞</span>;
      default:
        return <span className="emoji" role="img" aria-label="very sad">😢</span>;
    }
  }

  handleEmojiClick(e){
    console.log("Clicked! ", e.target);
  }

  render(){
    return (
      <GoogleMap
        defaultZoom={12}
        defaultCenter={{ lat: 40.712775 ,lng: -74.005973 }}
        defaultOptions={{ styles: MapStyles}}
        >
        {this.props.points?
          this.props.points.map((dataPoint) => {
            return (<OverlayView
              key={dataPoint.score}
              position={{ lat:dataPoint.lat, lng:dataPoint.long }}
              mapPaneName={OverlayView.OVERLAY_LAYER}>
              <div className="dataPoint">
                {this.getEmoji(dataPoint.score)}
              </div>
              </OverlayView>)
          })
          :null}
      </GoogleMap>


      // <svg className="map" viewBox="0 0 100 100">
      //   <polygon className="map-vector" points="12.417,28.583 11.25,29.917
      //     11.25,31.333 9.417,32.417 8.25,33.833 6.917,35.75 6.167,37.75 4.083,39.833 3.75,42.667 7,41.917 8,40.917 9.417,40.917
      //     8.833,43 7.667,45.833 8.25,48.75 6.083,50.083 5.083,51.25 8,58.417 10.167,61.083 13.167,64 16.333,65.25 19.25,69
      //     22.417,72.083 26.917,72.667 30.333,72.083 34.417,71.917 39.083,73.333 44.667,75.667 52.749,77.249 57.999,76.749 62.416,75.916
      //     62.832,74.499 67.332,72.583 70.249,73.166 74.999,71.166 81.416,64.833 82.249,60.249 82.832,56.333 84.666,56.333 83.416,54.833
      //     82.749,51.333 83.832,50.583 87.082,53.333 90.082,54.083 93.332,52.583 93.916,52.416 95.249,53.749 97.249,54.166 97.666,52.249
      //     98.749,50.749 98.082,49.333 94.332,47.75 94.916,45.583 94.082,44.083 89.416,42.75 86.749,43.333 85.916,44.833 81.749,46.833
      //     80.666,46.833 76.582,46 73.416,45.333 66.416,40.916 60.999,35.583 55.832,30.999 53.999,27.666 46.749,23 42.332,26.583
      //     42.249,28.75 36.499,28.75 36.332,25.333 34.749,24.666 32.499,25.333 31.582,26.833 27.749,27.083 23.749,29.25 17.916,29.5
      //     14.666,29.583 	"/>
      // </svg>
    )
  }

}

export default withScriptjs(withGoogleMap(Map));
