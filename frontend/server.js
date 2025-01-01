const express = require('express');
const bodyParser = require('body-parser');
const login = require('./functions/login/handler');
const logout = require('./functions/logout/handler');
const startRandomGame = require('./functions/startRandomGame/handler');
const makeMove = require('./functions/makeMove/handler');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
  });

app.post('/api/login', async (req, res) => {
    const response = await login.handler({body: JSON.stringify(req.body)})
    res.status(response.statusCode).send(response.body);
});

app.post('/api/logout', async (req, res) => {
    const response = await logout.handler()
    res.status(response.statusCode).send(response.body);
});

app.post('/api/game/start/random', async (req, res) => {
  const response = await startRandomGame.handler();
  res.status(response.statusCode).send(response.body);
});


app.post('/api/game/:gameId/move', async (req, res) => {
  const response = await makeMove.handler({ pathParameters: req.params, body: JSON.stringify(req.body)});
    res.status(response.statusCode).send(response.body);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});