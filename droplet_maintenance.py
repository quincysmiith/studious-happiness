import requests
import digitalocean
from time import sleep
import logging
import json
import os

current_location = os.path.dirname(os.path.realpath(__file__))

log_file = os.path.join(current_location, "maintain.log")

logging.basicConfig(filename=log_file, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

current_location = os.path.dirname(os.path.realpath(__file__))
key_file = os.path.join(current_location, 'key.json')

with open(key_file) as f:
    data = json.load(f)

key = data['key']


def softRestartDroplet(my_token):
    manager = digitalocean.Manager(token=my_token)
    droplet = manager.get_droplet(99020896)
    droplet.power_off()

    sleep(60)

    droplet.power_on()


def hardRestartDroplet(my_token):
    manager = digitalocean.Manager(token=my_token)
    droplet = manager.get_droplet(99020896)
    droplet.power_cycle()


attempt = True
count = 0
while attempt:
    try:
        status = requests.get('https://bubblevision.co')
    except Exception as e:
        count += 1
        sleep(30)
        if count > 5:
            logging.warning("can't contact site, performing force reboot")
            hardRestartDroplet(key)
            attempt = False
            logging.warning("force reboot complete.")

    if type(status.status_code) == int:
        if status.status_code == 200:
            logging.info("Site is up")
            attempt = False
        else:
            logging.warning("Didn't receive 200 status code, soft rebooting")
            softRestartDroplet(key)
            logging.warning("soft reboot complete")
            attempt = False
