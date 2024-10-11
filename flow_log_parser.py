import csv
from collections import defaultdict
import os

protocols = {
    'ip': 0,
    'hopopt': 0,
    'icmp': 1,
    'tcp': 6,
    'udp': 17,
    'ipv6': 41,
    'ipv6-icmp': 58,
    'ipv6-route': 43,
    'ipv6-frag': 44,
    'esp': 50,
    'ah': 51,
    'ospf': 89
}

def parse_lookup_table(lookup_file):
    lookup_table = defaultdict(list)
    with open(lookup_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dstport = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup_table[(dstport, protocol)].append(tag)
    return lookup_table

def parse_flow_logs(flow_log_file):
    flow_logs = []
    with open(flow_log_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 14:
                continue
            dstport = parts[6]
            protocol_number = parts[7]

            protocol = next((key for key, value in protocols.items() if str(value) == protocol_number), "unknown")
            flow_logs.append((dstport, protocol))
    return flow_logs

def map_tags(flow_logs, lookup_table):
    tag_count = defaultdict(int)
    port_protocol_count = defaultdict(int)
    untagged_count = 0

    for dstport, protocol in flow_logs:
        key = (dstport, protocol)
        if key in lookup_table:
            for tag in lookup_table[key]:
                tag_count[tag] += 1
            port_protocol_count[key] += 1
        else:
            untagged_count += 1

    tag_count['Untagged'] = untagged_count
    return tag_count, port_protocol_count

def write_output(tag_count, port_protocol_count, output_file):
    with open(output_file, 'w') as file:
        file.write("Tag Counts:\nTag,Count\n")
        for tag, count in tag_count.items():
            file.write(f"{tag},{count}\n")

        file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
        for (port, protocol), count in port_protocol_count.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lookup_file = os.path.join(base_dir, 'data/lookup_table.csv')
    flow_log_file = os.path.join(base_dir, 'data/flow_logs.txt')
    output_file = os.path.join(base_dir, 'output_report.txt')

    lookup_table = parse_lookup_table(lookup_file)
    print(lookup_table)
    flow_logs = parse_flow_logs(flow_log_file)
    #print(flow_logs)

    tag_count, port_protocol_count = map_tags(flow_logs, lookup_table)
    print(port_protocol_count)
    write_output(tag_count, port_protocol_count, output_file)

if __name__ == '__main__':
    main()
