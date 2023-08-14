from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "http://20.244.56.144"

# Replace with your actual credentials
COMPANY_NAME = "ECNAD"
CLIENT_ID = "b46118f0-fbde-4b16-a4b1-6ae6ad718627"
CLIENT_SECRET = "XoyolORPasKWODAN"
AUTH_TOKEN = None

def get_auth_token():
    global AUTH_TOKEN
    if AUTH_TOKEN:
        return AUTH_TOKEN

    auth_payload = {
        "companyName": COMPANY_NAME,
        "clientID": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }

    response = requests.post(f"{BASE_URL}/train/auth", json=auth_payload)
    if response.status_code == 200:
        AUTH_TOKEN = response.json()["access_token"]
        return AUTH_TOKEN
    else:
        return None

def get_all_trains():
    headers = {"Authorization": f"Bearer {get_auth_token()}"}
    response = requests.get(f"{BASE_URL}/train/trains", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

@app.route('/trains', methods=['GET'])
def get_train_schedules():
    all_trains = get_all_trains()

    current_time = 0  # Replace with actual current time in minutes since midnight

    filtered_trains = []
    for train in all_trains:
        if train["departureTime"]["Hours"] >= current_time // 60 + 1 and current_time <= 660:
            filtered_trains.append(train)

    sorted_trains = sorted(filtered_trains, key=lambda x: (
        x["price"]["sleeper"], -x["seatsAvailable"]["sleeper"], -x["seatsAvailable"]["AC"], -x["departureTime"]["Hours"] * 60 - x["departureTime"]["Minutes"]
    ))

    return jsonify(sorted_trains)

if __name__ == '__main__':
    app.run(debug=True)
