const AWS = require('aws-sdk');
const Chess = require("chess.js").Chess;

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = 'chess-games';


exports.handler = async (event) => {
  try {
    const body = JSON.parse(event.body);
    console.log("body123");
    console.log(body);
    console.log(body["piece"]);
    const piece = body.piece;



    const gameId = event.pathParameters.gameId;
    const params = {
      TableName: tableName,
      Key: {
        gameId: gameId
      }
    };

    const result = await dynamoDB.get(params).promise();

    if (!result.Item) {
      return {
        statusCode: 404,
        body: JSON.stringify({ message: 'Game not found' }),
      };
    }

    const game = new Chess(result.Item.fen);

    // do not pick up pieces if the game is over
    if (game.isGameOver()) {
      return {
        statusCode: 200,
        body: JSON.stringify({ canPickUpPiece: false }),
      };
    }

    // only pick up pieces for the side to move
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
      return {
        statusCode: 200,
        body: JSON.stringify({ canPickUpPiece: false }),
      };
    }
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: 'Internal server error' }),
    };
  }
};