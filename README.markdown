# Scylla VPN

*Author*: elryan7\
*Repository*: https://github.com/elryan7/scylla-vpn\
*License*: MIT

## Description

Scylla VPN is a professional-grade VPN solution supporting OpenVPN and WireGuard protocols, with AES-256 encryption, a kill switch, and a modern web interface for management. Designed to compete with commercial solutions like NordVPN or ProtonVPN, it offers secure, scalable, and customizable VPN services for individuals, teams, or enterprises.

## Features

- Multi-protocol support (OpenVPN, WireGuard)
- AES-256 encryption with secure key management
- Kill switch to prevent data leaks
- Web interface for server and user management (Flask, Tailwind CSS)
- Docker support for easy deployment
- Protection against DNS leaks
- Scalable multi-server architecture
- Minimal logging for user privacy

## Prerequisites

- Python 3.8+
- Libraries: `flask`, `jinja2`, `pydantic`
- OpenVPN and WireGuard installed on the server
- Docker (optional, for containerized deployment)
- Node.js and Tailwind CSS (for web interface styling)
- Root/admin privileges for VPN setup and kill switch

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/elryan7/scylla-vpn.git
   cd scylla-vpn
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   npm install tailwindcss
   npm run build:css
   ```
3. Install OpenVPN and WireGuard:

   ```bash
   sudo apt-get install openvpn wireguard
   ```
4. Run setup scripts:

   ```bash
   sudo bash scripts/setup_openvpn.sh
   sudo bash scripts/setup_wireguard.sh
   ```
5. (Optional) Build and run with Docker:

   ```bash
   docker build -t scylla-vpn .
   docker run -p 5000:5000 --privileged scylla-vpn
   ```

## Usage

### Web Interface

Run the Flask server:

```bash
python3 app.py
```

Access the interface at `http://localhost:5000`.

### CLI

Start the VPN server:

```bash
sudo python3 scylla_vpn.py --protocol openvpn
```

- `--protocol`: Choose `openvpn` or `wireguard`.
- Logs are saved to `scylla_vpn.log`.

### Client Configuration

1. Download client configuration files from the web interface (`/dashboard`).
2. Use OpenVPN Connect or WireGuard client to connect.

## Example Output

```log
2025-07-22 14:26:36 - Scylla VPN started with OpenVPN protocol
2025-07-22 14:26:37 - Client connected: 192.168.1.100
2025-07-22 14:26:38 - Kill switch enabled
```

## Project Structure

- `app.py`: Flask web server for the interface
- `scylla_vpn.py`: Core VPN logic (configuration, management)
- `configs/`: Configuration files for OpenVPN and WireGuard
- `scripts/`: Setup scripts for VPN and kill switch
- `templates/`: Jinja2 templates for the web interface
- `static/`: CSS and JS files (Tailwind CSS)
- `vpn_config.json`: Global VPN configuration
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker configuration
- `package.json`: Node.js dependencies for Tailwind CSS
- `scylla_vpn.log`: Log file for connections and errors

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on GitHub.

## Disclaimer

This tool is for educational and authorized use only. Ensure compliance with local laws and regulations when deploying or using the VPN.