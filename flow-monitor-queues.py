#!/usr/bin/python
import json
import subprocess

data = []

command = "FLOW_CONTEXT=Production /usr/bin/php /var/www/html/flow queue:list"

process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
result = process.stdout.read()

if result.stdout: 
    lines = result.stdout.splitlines();
    del lines[0:3]
    del lines[-1]

    for line in lines:
        parts = line.decode().split('|');

        queueName = parts[1].strip()
        jobsCount = int(parts[3])

        data.append({
            'queue': queueName, 
            'jobs' : jobsCount
        });

print(json.dumps(data, indent=4, sort_keys=True))

