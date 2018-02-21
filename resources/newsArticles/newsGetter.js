var fs = require('fs');
var path = require('path');

const apiKey = "5a1c7505c033431ba8ec42dae2396411" //fs.readFileSync(jsonPath, 'utf8');

const NewsAPI = require('newsapi');
const newsapi = new NewsAPI(apiKey);

// To query top headlines
// All options passed to topHeadlines are optional, but you need to include at least one of them
newsapi.v2.everything({
  q: 'scotland',
  language: 'en',
  from: '2016-5-01',
  to: '2017-6-01',
}).then(response => {
  console.log(response);
  /*
    {
      status: "ok",
      articles: [...]
    }
  */
});
