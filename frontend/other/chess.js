const Chess = require("chess.js").Chess;
const { v4: uuidv4 } = require('uuid');

exports.handler = async (event) => {
  const gameId = uuidv4();
  const game = new Chess();
    
  return {
    statusCode: 200,
    body: JSON.stringify({ gameId: gameId, fen: game.fen() }),
  };
};