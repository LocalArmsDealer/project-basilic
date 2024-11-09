# Copyright (C) 2024 Alina
# Project Basilic uses the GNU Public License (GPLv3). Details are available in the LICENSE file contained in the "Project Basilic" folder.
import json
import socket
import logging
import os
from datetime import datetime

# JSON config loader
with open('../config.json') as config_file:
    config = json.load(config_file)

d_ip = config['drone_ip']
d_port = config['drone_port']
logtype = config['log_level']
log_folder = config['log_folder']
timeout = config['timeout']

# Log folder maker (for redundancy)
os.makedirs(log_folder, exist_ok=True)

# Log file name picker
c_time = datetime.now().strftime("%d%m%y-%H%M")
log_name = f"{log_folder/{c_time}.log}"

# Log file maker
logging.basicConfig(
    filename=log_name,
    level=logtype,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_command(command):
    """Send a JavaScript command to the drone via UDP."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        # Drone command sender
        sock.sendto(command.encode(), (d_ip, d_port))

        # Drone data receiver
        response, _ = sock.recvfrom(1024)

        # Drone response logger
        logging.info(f"{command} sent, {response.decode()} received.")
        return response.decode()
    
    except socket.timeout:
        logging.error("Timeout occured while awaiting drone response.")
        logging.info("Attempting to send landing command to drone.")
        send_command("land()")
        return "Timeout - Landing command sent"
    
    except socket.error as e:
        logging.error(f"Socket error: {e}")
        logging.info("Attempting to send landing command to drone.")
        send_command("land()")
        return "Socket error - Landing command sent"
    
    except Exception as e:
        logging.error(f"Error: {e}")
        return str(e)
    
    finally:
        sock.close()
