var express = require('express');
const { compile } = require('pug/lib');
var router = express.Router();

const { spawn } = require('child_process');

router.get('/get_content_check/', function(req, res) {
    let headline = req.body.headline;
    let content = req.body.content;
    let result = {"SPEECH":"NA","DETECT":"NA"};
    const pythonProcess = spawn('python', ['models/hate_speech_api.py', headline, content]);
    pythonProcess.stdout.on('data', (data) => {
        result["SPEECH"] = data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(data.toString());
        res.send(result);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        const pythonProcess1 = spawn('python', ['models/ai_detect_api.py', headline, content]);
        pythonProcess1.stdout.on('data', (data) => {
            result["DETECT"] = data.toString();
        });

        pythonProcess1.stderr.on('data', (data) => {
            console.error(data.toString());
            res.send(result);
        });

        pythonProcess1.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
            res.send(result);
        });
    });
});


module.exports = router;

// Path: app.js
// Compare this snippet from app.js:
// // include routes
// http://localhost:8000/get_article_recommend/[7595,12554]&[WORLD,POLITICS,SPORTS]