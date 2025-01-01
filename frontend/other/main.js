// Import the Serverless framework libraries and Express
const express = require('express');
const serverless = require('serverless-http');

// Initialize the Express app
const app = express();
app.use(express.json()); // Middleware for parsing JSON requests

// Example route to handle requests
app.get('/hello', (req, res) => {
  res.json({ message: 'Hello, Serverless World!' });
});

app.post('/data', (req, res) => {
  const { name, age } = req.body;
  res.json({ message: `Received data for ${name}, age ${age}.` });
});

// Export the app and use the serverless-http adapter for deployment
module.exports.handler = serverless(app);
 