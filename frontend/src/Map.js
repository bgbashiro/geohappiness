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
    switch(Number(score)) {
      case (0):
        return <span className="emoji" role="img" aria-label="very sad">😢</span>;
      case (1):
        return <span className="emoji" role="img" aria-label="sad">😑</span>;
      case (2):
        return <span className="emoji" role="img" aria-label="very happy">😄</span>;
      default:
        return <span className="emoji" role="img" aria-label="sad">😞</span>;
    }
  }

  handleEmojiClick(e){
    console.log("Clicked! ", e.target);
  }

  render(){
    return (
      <GoogleMap
        defaultZoom={10}
        defaultCenter={{ lat: 40.712775 ,lng: -74.005973 }}
        defaultOptions={{ styles: MapStyles}}
        >
        {this.props.points?
          this.props.points.map((dataPoint) => {
            return (<OverlayView
              key={dataPoint.long}
              position={{ lat:dataPoint.long, lng:dataPoint.lat }}
              mapPaneName={OverlayView.OVERLAY_LAYER}>
              <div className="dataPoint">
                {this.getEmoji(dataPoint.score)}
              </div>
              </OverlayView>)
          })
          :null}
      </GoogleMap>
    )
  }

}

export default withScriptjs(withGoogleMap(Map));
