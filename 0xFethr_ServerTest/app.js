// include routes 
var article_recommender = require('./routes/article_recommender.js');
var content_check = require('./routes/content_check.js');
var express = require('express');
var app = express();


app.use(express.json()); // add this line to parse incoming JSON data
app.use(express.urlencoded({ extended: false })); // add this line to parse incoming URL-encoded data

app.get('/', function(req, res) {
    res.send('API initialized');
});

app.listen(8000, function() {
    console.log('Express server listening on port 8000');
});

app.post('/add_new_article/', article_recommender);

app.get('/get_article_recommend/', article_recommender);

app.get('/get_content_check/', content_check);


