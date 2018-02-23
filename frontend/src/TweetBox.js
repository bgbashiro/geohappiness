import React from 'react';
import TwitterIcon from 'react-icons/lib/fa/twitter-square';

const TweetBox = (props) => {
  return (
    <div className="tweet">
      <p>
        <TwitterIcon size={25} color="#33FFE1" style={{
              margin: "0 0.5em 0.5em 0"
            }}/>
        {props.text}
      </p>
    </div>
  )
}

export default TweetBox;
