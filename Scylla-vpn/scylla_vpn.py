import subprocess
import json
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(filename='scylla_vpn.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def setup_openvpn():
    """Run OpenVPN setup script."""
    try:
        subprocess.run(['bash', 'scripts/setup_openvpn.sh'], check=True)
        logging.info("OpenVPN setup completed")
    except subprocess.CalledProcessError as e:
        logging.error(f"OpenVPN setup failed: {e}")

def setup_wireguard():
    """Run WireGuard setup script."""
    try:
        subprocess.run(['bash', 'scripts/setup_wireguard.sh'], check=True)
        logging.info("WireGuard setup completed")
    except subprocess.CalledProcessError as e:
        logging.error(f"WireGuard setup failed: {e}")

def enable_kill_switch():
    """Enable kill switch to prevent data leaks."""
    try:
        subprocess.run(['bash', 'scripts/kill_switch.sh', 'enable'], check=True)
        logging.info("Kill switch enabled")
    except subprocess.CalledProcessError as e:
        logging.error(f"Kill switch enable failed: {e}")

def disable_kill_switch():
    """Disable kill switch."""
    try:
        subprocess.run(['bash', 'scripts/kill_switch.sh', 'disable'], check=True)
        logging.info("Kill switch disabled")
    except subprocess.CalledProcessError as e:
        logging.error(f"Kill switch disable failed: {e}")

def start_vpn(protocol, server_ip):
    """Start VPN server with specified protocol."""
    if protocol == 'openvpn':
        config_file = 'configs/openvpn.conf'
        subprocess.run(['openvpn', '--config', config_file, '--daemon'], check=True)
    elif protocol == 'wireguard':
        config_file = 'configs/wireguard.conf'
        subprocess.run(['wg-quick', 'up', config_file], check=True)
    logging.info(f"VPN started with {protocol} on {server_ip}")
    enable_kill_switch()

def stop_vpn():
    """Stop VPN server."""
    try:
        subprocess.run(['pkill', 'openvpn'], check=True)
        subprocess.run(['wg-quick', 'down', 'configs/wireguard.conf'], check=True)
        disable_kill_switch()
        logging.info("VPN stopped")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to stop VPN: {e}")

def get_vpn_status():
    """Check VPN server status."""
    try:
        openvpn_status = subprocess.run(['pgrep', 'openvpn'], capture_output=True, text=True).returncode == 0
        wireguard_status = subprocess.run(['wg', 'show'], capture_output=True, text=True).returncode == 0
        return {
            'openvpn': openvpn_status,
            'wireguard': wireguard_status,
            'kill_switch': subprocess.run(['iptables', '-L'], capture_output=True, text=True).stdout
        }
    except Exception as e:
        logging.error(f"Error checking VPN status: {e}")
        return {'error': str(e)}

def generate_client_config(protocol, server_ip):
    """Generate client configuration file."""
    config_dir = 'configs'
    if protocol == 'openvpn':
        config_file = f"{config_dir}/client.ovpn"
        with open(config_file, 'w') as f:
            f.write(f"""
client
dev tun
proto udp
remote {server_ip} 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
cipher AES-256-CBC
verb 3
""")
    elif protocol == 'wireguard':
        config_file = f"{config_dir}/client.conf"
        with open(config_file, 'w') as f:
            f.write(f"""
[Interface]
PrivateKey = <client-private-key>
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = <server-public-key>
Endpoint = {server_ip}:51820
AllowedIPs = 0.0.0.0/0, ::/0
""")
    logging.info(f"Generated {protocol} client config: {config_file}")
    return config_file

def main(protocol='openvpn'):
    """Main function for Scylla VPN."""
    if protocol == 'openvpn':
        setup_openvpn()
    elif protocol == 'wireguard':
        setup_wireguard()
    
    with open('vpn_config.json', 'r') as f:
        config = json.load(f)
    
    server_ip = config['servers'][0]['ip'] if config['servers'] else '127.0.0.1'
    start_vpn(protocol, server_ip)
    print(f"Scylla VPN started with {protocol}. Access dashboard at http://localhost:5000.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scylla VPN")
    parser.add_argument('--protocol', choices=['openvpn', 'wireguard'], default='openvpn', help="VPN protocol")
    args = parser.parse_args()
    
    main(args.protocol)