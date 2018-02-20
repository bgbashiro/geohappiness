var fs = require('fs');
var path = require('path');

const apiKey = "" //fs.readFileSync(jsonPath, 'utf8');

const NewsAPI = require('newsapi');
const newsapi = new NewsAPI(apiKey);

// To query top headlines
// All options passed to topHeadlines are optional, but you need to include at least one of them
newsapi.v2.topHeadlines({
  q: '',
  language: 'en',
  country: 'us'
}).then(response => {
  console.log(response);
  /*
    {
      status: "ok",
      articles: [...]
    }
  */
});
