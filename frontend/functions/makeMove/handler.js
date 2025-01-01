const AWS = require('aws-sdk');
const Chess = require("chess.js").Chess;

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const tableName = 'chess-games';


exports.handler = async (event) => {
  try {
      const gameId = event.pathParameters.gameId;
      const { move } = JSON.parse(event.body);
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

        // Validate the Move
        try{
          const chessMove = game.move(move);
          if(!chessMove){
             return {
                statusCode: 400,
                body: JSON.stringify({message: "invalid move"})
            }
        }
        }catch{
          return {
            statusCode: 400,
            body: JSON.stringify({message: "invalid move"})
        }
      }


     const updateParams = {
          TableName: tableName,
            Key: {
             gameId: gameId
           },
         UpdateExpression: 'set fen = :fen',
         ExpressionAttributeValues: {
             ':fen': game.fen(),
         },
      }
      await dynamoDB.update(updateParams).promise()

      return {
        statusCode: 200,
        body: JSON.stringify({ fen: game.fen() }),
      };
    } catch (error) {
      console.error(error);
      return {
        statusCode: 500,
        body: JSON.stringify({ message: 'Internal server error' }),
      };
   }
};