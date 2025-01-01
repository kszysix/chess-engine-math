exports.handler = async (event) => {
    const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess Engine Math</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Welcome to Chess Engine Math 2</h1>
    </header>
    <main>
        <p>This is a basic Node.js application for a chess engine.</p>
    </main>
    <footer>
        <p>&copy; 2023 Chess Engine Math</p>
    </footer>
    <script src="app.js"></script>
</body>
</html>
    `;
    
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'text/html',  // Set the content type to HTML
        },
        body: htmlContent,  // Return the HTML content as the body
    };
};
