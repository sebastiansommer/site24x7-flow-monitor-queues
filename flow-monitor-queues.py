#!/usr/bin/python
import json
import subprocess

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

FLOW_PATH = "FLOW_CONTEXT=Production /usr/bin/php /var/www/flow queue:list"

class FlowQueues(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None

    def collectData(self):
        data = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
            'units': {}
        }

        process = subprocess.Popen(FLOW_PATH, shell=True, stdout=subprocess.PIPE)
        result = process.stdout.read()

        lines = result.splitlines();

        del lines[0:3]
        del lines[-1]

        for line in lines:
            parts = line.decode().split('|');

            queueName = parts[1].strip()
            jobsCount = int(parts[3])

            indexName = 'queue-' + queueName

            data[indexName] = jobsCount

            data['units'][indexName] = 'count'
        return data

if __name__ == "__main__":
    configurations = {}
    plugin = FlowQueues(configurations)
    result = plugin.collectData()
    print(json.dumps(result, indent=4, sort_keys=True))
