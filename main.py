from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
upload_log = []
manual_water_flag = False

@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.get_json()
    humidity = data.get('humidity')
    watered = data.get('watered')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    upload_log.append({
        'time': timestamp,
        'humidity': humidity,
        'watered': watered
    })
    print(f"[UPLOAD] {timestamp} 濕度={humidity}, 澆水={watered}")
    return jsonify({"status": "ok"})

@app.route('/api/water_now', methods=['POST'])
def water_now():
    global manual_water_flag
    manual_water_flag = True
    return jsonify({'status': 'triggered'})

@app.route('/api/check_water_command', methods=['GET'])
def check_water_command():
    global manual_water_flag
    if manual_water_flag:
        manual_water_flag = False
        return jsonify({'water_now': True})
    return jsonify({'water_now': False})

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html>
    <head><title>澆水系統控制面板</title></head>
    <body>
        <h2>🌱 自動澆水系統</h2>
        <button onclick="fetch('/api/water_now', {method:'POST'})">手動澆水</button>
        <h3>最近紀錄</h3>
        <ul>
            {% for record in logs[-5:] %}
                <li>{{ record.time }} - 濕度: {{ record.humidity }} - 澆水: {{ record.watered }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html, logs=upload_log)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
