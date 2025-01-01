const Chess = require("chess.js").Chess;
const { v4: uuidv4 } = require('uuid');
const AWS = require('aws-sdk');


const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = 'chess-games';

exports.handler = async (event) => {
  try {
      const gameId = uuidv4();
      const game = new Chess();

      const params = {
          TableName: tableName,
          Item: {
              gameId: gameId,
              fen: game.fen()
          }
      };

      await dynamoDB.put(params).promise()

      return {
          statusCode: 200,
          body: JSON.stringify({ gameId: gameId, fen: game.fen() }),
      };
  } catch (error) {
      console.error(error);
      return {
          statusCode: 500,
          body: JSON.stringify({ message: 'Internal server error' }),
      };
  }
};