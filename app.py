from flask import Flask, request, jsonify
import requests
import random
import time

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h1>Warpcast Auto Like</h1>
        <form action="/submit" method="post">
            Token: <input type="text" name="token"><br>
            Targets (comma separated): <input type="text" name="targets"><br>
            Min Delay: <input type="text" name="min_delay"><br>
            Max Delay: <input type="text" name="max_delay"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    token = request.form['token']
    targets = request.form['targets'].split(',')
    min_delay = int(request.form['min_delay'])
    max_delay = int(request.form['max_delay'])

    results = []

    for idx, target in enumerate(targets, start=1):
        result = send_like(target.strip(), token)
        results.append(result)

        delay = random.randint(min_delay, max_delay)
        time.sleep(delay)

    return jsonify(results)

def send_like(target, token):
    like_url = f"{target}/like"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(like_url, headers=headers)

    return {
        "target": target,
        "status_code": response.status_code,
        "response_text": response.text
    }

if __name__ == '__main__':
    app.run(debug=True)
