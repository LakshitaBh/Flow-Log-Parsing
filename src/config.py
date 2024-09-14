LOOKUP_FILEPATH = '../data/lookup.csv'
FLOW_LOG_FILEPATH = '../data/flowlogs.txt'
OUTPUT_FILEPATH = '../data/output/report.txt'
CUSTOM_FLOW_LOG_FIELDS = ['srcaddr', 'dstaddr', 'srcport', 'dstport', 'protocol', 'packets', 'bytes', 'start', 'end', 'action', 'log-status']
PROTOCOL_NUMBER_TO_NAME = {
    1: 'icmp',
    6: 'tcp',
    17: 'udp'
}