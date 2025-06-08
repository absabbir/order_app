from flask import Flask, request, render_template_string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from waitress import serve  # এখানে waitress যুক্ত করুন

app = Flask(__name__)

# Google Sheets API setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1zJ6pi8PKa-udFofQkv3Ttuu3op1TnqrzltoQMxfe9cE/edit#gid=0").sheet1

# HTML form
html_form = '''
<!DOCTYPE html>
<html>
<head>
  <title>Order Form</title>
  <style>
    body { font-family: Arial; padding: 20px; max-width: 400px; margin: auto; }
    input, select { width: 100%; padding: 10px; margin: 5px 0; }
    button { padding: 10px; width: 100%; background: purple; color: white; border: none; }
  </style>
</head>
<body>
  <h2>📦 অর্ডার ফর্ম</h2>
  <form action="/submit" method="post">
    <label>👤 নাম:</label>
    <input type="text" name="name" required>

    <label>📱 মোবাইল:</label>
    <input type="text" name="phone" required>

    <label>🏠 ঠিকানা:</label>
    <input type="text" name="address" required>

    <label>📏 সাইজ:</label>
    <select name="size" required>
      <option value="Small">Small</option>
      <option value="Large">Large</option>
      <option value="Teen">Teen</option>
    </select>

    <button type="submit">✅ অর্ডার করুন</button>
  </form>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_form)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    size = request.form['size']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([name, phone, address, size, time])
    return f"ধন্যবাদ {name}! আপনার অর্ডার নেওয়া হয়েছে। ✅"

# Waitress দিয়ে অ্যাপ চালানো
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)  # এখানে waitress দিয়ে অ্যাপ চালানো হচ্ছে
