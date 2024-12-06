from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simple HTML template
html_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Quick CSV Offer Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f7f7f7;
        }
        .container {
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
        h1 {
            margin-top: 0;
            text-align: center;
        }
        form {
            margin-top: 20px;
        }
        input[type=file] {
            display: block;
            margin: 20px 0;
        }
        button {
            background: #2c3e50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #1a252f;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.9em;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CSV Offer Bot</h1>
        <p>Upload your CSV file of listings and the bot will process it to send automated offer emails on your behalf.</p>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="csvFile">Select CSV file:</label>
            <input type="file" id="csvFile" name="file" accept=".csv" required>
            <button type="submit">Process CSV</button>
        </form>

        <div class="footer">
            <p>&copy; 2024 Your Company</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_template)

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        # For now, just show a message that the file was received.
        return f"CSV file '{file.filename}' received and would be processed."
    else:
        return "Please upload a valid CSV file."

if __name__ == "__main__":
    # Run the Flask app on a standard port
    app.run(host='0.0.0.0', port=8080)
