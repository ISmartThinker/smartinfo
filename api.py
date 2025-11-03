from flask import Flask, jsonify, request
import requests
import threading
import time

SmartEyecone = Flask(__name__)

def fetch_number_info(cli, storage):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'application/json',
        'e-auth-v': 'e1',
        'e-auth': 'c5f7d3f2-e7b0-4b42-aac0-07746f095d38',
        'e-auth-c': '40',
        'e-auth-k': 'PgdtSBeR0MumR7fO',
        'accept-charset': 'UTF-8',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Host': 'api.eyecon-app.com',
        'Connection': 'Keep-Alive'
    }
    params = {
        'cli': cli,
        'lang': 'en',
        'is_callerid': 'true',
        'is_ic': 'true',
        'cv': 'vc_672_vn_4.2025.10.17.1932_a',
        'requestApi': 'URLconnection',
        'source': 'MenifaFragment'
    }
    try:
        r = requests.get('https://api.eyecon-app.com/app/getnames.jsp', params=params, headers=headers, timeout=15)
        try:
            storage['raw'] = r.json()
        except ValueError:
            storage['raw'] = r.text
        storage['status_code'] = r.status_code
    except Exception as e:
        storage['raw'] = {'error': str(e)}
        storage['status_code'] = 500

@SmartEyecone.route('/')
def docs():
    return jsonify({
        'api_docs': '/api/num?value={number}',
        'example': '/api/num?value=01991079807 or /api/num?value=+8801991079807',
        'api_owner': '@ISmartCoder',
        'api_updates': '@abirxdhackz',
        'api_base': '@SomawDev'
    })

@SmartEyecone.route('/api/num')
def get_number_info():
    start = time.time()
    value = request.args.get('value', '')
    if value.startswith('+880'):
        cli = value.replace('+880', '880')
    elif value.startswith('0'):
        cli = '88' + value
    else:
        cli = value
    storage = {}
    thread = threading.Thread(target=fetch_number_info, args=(cli, storage))
    thread.start()
    thread.join()
    raw = storage.get('raw', {})
    status = storage.get('status_code', 200)
    metadata = {
        'api_owner': '@ISmartCoder',
        'api_updates': '@abirxdhackz',
        'api_base': '@SomawDev',
        'time_taken': round(time.time() - start, 3)
    }
    if isinstance(raw, dict):
        merged = {**raw, **metadata}
        return jsonify(merged), status
    elif isinstance(raw, list):
        payload = {'results': raw, **metadata}
        return jsonify(payload), status
    else:
        payload = {'response': raw, **metadata}
        return jsonify(payload), status

# For local development
if __name__ == '__main__':
    SmartEyecone.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

# Required by Vercel
app = SmartEyecone
