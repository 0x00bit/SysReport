from flask import Flask, render_template, jsonify
import redis
import json
from datetime import datetime

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_panels():
    panels = {}
    categories = ['PAINEL_STATUS', 'TOTEM_STATUS']

    for cat in categories:
        try:
            data = r.hgetall(cat)
            hosts = []
            for hostname, value in data.items():
                parsed = json.loads(value)
                parsed["status"] = int(parsed.get("status", 0))
                hosts.append(parsed)
            panels[cat] = hosts
        except Exception as e:
            print(f"Erro ao ler {cat}: {e}")
    return panels

@app.route('/')
def index():
    panels = get_panels()
    return render_template('index.html', panels=panels)

@app.route('/api/status')
def api_status():
    return jsonify({
        "data": get_panels(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
