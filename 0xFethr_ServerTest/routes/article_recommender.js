var express = require('express');
const { compile } = require('pug/lib');
var router = express.Router();

const { spawn } = require('child_process');
// const pythonProcess = spawn('python', ['hellopath/to/python/file.py']);//, arg1, arg2]);

router.post('/add_new_article/', function(req, res) {
    let headline = req.body.headline;
    let category = req.body.category;
    let authors = req.body.authors;
    let id = req.body.id;
    let date = req.body.date;
    const pythonProcess = spawn('python', ['models/data_maintainer.py', headline, category, authors, id, date]);
    let process = "Success1";
    pythonProcess.stdout.on('data', (data) => {
        console.log(data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(data.toString());
        process = "Crash1";
        res.send(process);
    });

    process = "Success2";

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        
        const pythonProcess1 = spawn('python', ['models/generate_encoded_headlines_vocalbulary.py']);
        
        pythonProcess1.stdout.on('data', (data) => {
            console.log(data.toString());
        });

        pythonProcess1.stderr.on('data', (data) => {
            console.error(data.toString());
            process = "Crash2";
            res.send(process);
        });

        pythonProcess1.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
            res.send(process);
        });
    });

    
});


router.get('/get_article_recommend/', function(req, res) {
    let article_ids = req.body.article_ids;
    article_ids = article_ids.substring(1, article_ids.length - 1);
    let user_categories = req.body.user_categories;
    user_categories = user_categories.substring(1, user_categories.length - 1);
    article_ids = article_ids.split(',').map(String);
    user_categories = user_categories.split(',').map(String);
    let recommendations = [];

    const pythonProcess = spawn('python', ['models/recommender.py', article_ids, user_categories]);
    pythonProcess.stdout.on('data', (data) => {
        recommendations = data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(data.toString());
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        res.send(recommendations);
    });
});


module.exports = router;

// Path: app.js
// Compare this snippet from app.js:
// // include routes
// http://localhost:8000/get_article_recommend/[7595,12554]&[WORLD,POLITICS,SPORTS]