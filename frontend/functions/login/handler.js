// For simplicity, we'll use in-memory user management.
const users = {
    'user1': 'pass1',
    'user2': 'pass2',
  };
  const { v4: uuidv4 } = require('uuid');
  
  exports.handler = async (event) => {
    try {
      const { username, password } = JSON.parse(event.body);
  
      if (users[username] && users[username] === password) {
        const token = uuidv4(); // Generate a simple token
        // In a real app, you would typically use JWTs and store the token in a database
        return {
          statusCode: 200,
          body: JSON.stringify({ token }),
        };
      } else {
        return {
          statusCode: 401,
          body: JSON.stringify({ message: 'Invalid credentials' }),
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