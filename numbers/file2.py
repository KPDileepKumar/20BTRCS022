from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

def fetch_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return set(response.json().get("numbers", []))
    except requests.Timeout:
        pass
    return set()

@app.route('/numbers', methods=['GET'])
def get_merged_numbers():
    urls = request.args.getlist('url')
    merged_numbers = set()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_numbers_from_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            numbers = future.result()
            merged_numbers.update(numbers)

    sorted_numbers = sorted(merged_numbers)
    return jsonify({"numbers": sorted_numbers})

if __name__ == '__main__':
    app.run(debug=True, port=3000)


