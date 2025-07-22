from flask import Flask, render_template, request, send_file
import json
from scylla_vpn import start_vpn, stop_vpn, get_vpn_status, generate_client_config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    status = get_vpn_status()
    with open('vpn_config.json', 'r') as f:
        config = json.load(f)
    return render_template('dashboard.html', status=status, servers=config['servers'])

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        protocol = request.form['protocol']
        server_ip = request.form['server_ip']
        with open('vpn_config.json', 'r+') as f:
            config = json.load(f)
            config['servers'].append({'ip': server_ip, 'protocol': protocol})
            f.seek(0)
            json.dump(config, f, indent=4)
        start_vpn(protocol, server_ip)
        return render_template('config.html', message="Server added and started")
    return render_template('config.html')

@app.route('/download-config/<protocol>/<server_ip>')
def download_config(protocol, server_ip):
    config_file = generate_client_config(protocol, server_ip)
    return send_file(config_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)