from flask import Flask, request, render_template_string
import pandas as pd
from io import StringIO

app = Flask(__name__)

def calculate_buy_price(list_price):
    # Example: Offer 85% of the list price
    return round(list_price * 0.85, 2)

def generate_email(agent_name, address, list_price, buy_price):
    subject = f"Offer for {address}"
    body = f"""
Hi {agent_name},

We noticed the property at {address}, listed at ${list_price:,.2f}, and we would like to present an offer of ${buy_price:,.2f}.

Please let us know if you have any questions or need additional information.

Best,
Your Company
"""
    return subject, body

def send_email(agent_email, subject, body):
    # For now, we just print the email content to the console.
    # Later, you can integrate with a real email service.
    print("-----")
    print("Sending email to:", agent_email)
    print("Subject:", subject)
    print(body)
    print("-----")

# HTML template for the landing page
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
        data = file.read().decode('utf-8', errors='replace')
        df = pd.read_csv(StringIO(data))

        # Iterate over each listing in the CSV
        for _, row in df.iterrows():
            # Adjust these keys if your CSV columns differ
            agent_name = row.get('List Agent Full Name', 'Agent')
            agent_email = row.get('List Agent Email', 'test@example.com')
            address = row.get('Address', 'Unknown Address')
            
            list_price_str = row.get('Current Price', '0')
            # Remove $ and commas from the price
            list_price_str = list_price_str.replace('$', '').replace(',', '')
            try:
                list_price = float(list_price_str)
            except ValueError:
                list_price = 0.0

            # Calculate the buy price
            buy_price = calculate_buy_price(list_price)

            # Generate email subject and body
            subject, body = generate_email(agent_name, address, list_price, buy_price)

            # "Send" the email by printing to console
            send_email(agent_email, subject, body)

        return "CSV processed and emails were printed to the console."
    else:
        return "Please upload a valid CSV file."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
