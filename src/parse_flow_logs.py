import csv
from exceptions import *
import os
from config import *
import argparse
import datetime

class LookupTable:
    def __init__(self, filename:str):
        self._filename = filename
        if not self._valid_filename():
            raise InvalidFilenameError(filename)
        self._table = self._load_table()

    def _valid_filename(self)->bool:
        return os.path.exists(self._filename)

    def _load_table(self)->dict:
        table = {}
        with open(self._filename, 'r') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
            for row in reader:
                if not row:
                    continue
                key = (int(row['dstport'].strip()), row['protocol'].strip().lower())
                value = row['tag'].strip()
                table[key] = value
        return table
        

    def lookup(self, key:tuple)->str:
        # key (tuple): (dstport, protocol)
        return self._table.get(key, 'Untagged')

class FlowLog:
    def __init__(self, log_format:str='default', lookup_table:LookupTable=None):
        self._log_format = log_format.lower()
        if lookup_table is None:
            raise LookupTableError
        self._lookup_table = lookup_table
        self._tag_cnt = {}
        self._port_protocol_cnt = {}
        self._PROTOCOL_NUMBER_TO_NAME = PROTOCOL_NUMBER_TO_NAME

    def _valid_filename(self)->bool:
        return os.path.exists(self._filename)

    def parse_logs(self, filepath:str)->None:
        if self._log_format == 'default':
            self._parse_default_logs(filepath)
        elif self._log_format == 'custom':
            self._parse_custom_logs(filepath)
        else:
            raise InvalidLogFormatError(self._log_format)
    
    def _parse_default_logs(self, filepath:str)->None:
        with open(filepath, 'r') as f:
            for row in f:
                row = row.strip()
                if not row:
                    continue
                fields = row.split()
                print(fields)
                dstport = int(fields[6].strip())
                protocol = self._PROTOCOL_NUMBER_TO_NAME.get(int(fields[7].strip()), 'unknown')
                tag = self._lookup_table.lookup((dstport, protocol))
                self._tag_cnt[tag] = self._tag_cnt.get(tag, 0) + 1
                self._port_protocol_cnt[(dstport, protocol)] = self._port_protocol_cnt.get((dstport, protocol), 0) + 1

    def _parse_custom_logs(self, filepath:str)->None:
        for i, field in enumerate(CUSTOM_FLOW_LOG_FIELDS):
            if field == 'dstport':
                dstport_index = i
            elif field == 'protocol':
                protocol_index = i

        with open(filepath, 'r') as f:
            for row in f:
                row = row.strip()
                if not row:
                    continue
                fields = row.strip().split()
                dstport = int(fields[dstport_index].strip())
                protocol = self._PROTOCOL_NUMBER_TO_NAME.get(int(fields[protocol_index].strip()), 'unknown')
                tag = self._lookup_table.lookup((dstport, protocol))
                self._tag_cnt[tag] = self._tag_cnt.get(tag, 0) + 1
                self._port_protocol_cnt[(dstport, protocol)] = self._port_protocol_cnt.get((dstport, protocol), 0) + 1

    def get_tag_count(self)->dict:
        return self._tag_cnt

    def get_port_protocol_count(self)->dict:
        return self._port_protocol_cnt

class ReportGenerator:
    def __init__(self, output_filepath:str):
        current_date = datetime.date.today()
        formatted_date = current_date.strftime('%Y-%m-%d')
        self._output_filepath = self._get_full_filepath(output_filepath, formatted_date)

    def _get_full_filepath(self, base_filepath:str, formatted_date:str) -> str:
        base_dir = os.path.dirname(base_filepath)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        filename = f"report_{formatted_date}.txt"
        return os.path.join(base_dir, filename)

    def generate_report(self, tag_cnt:dict, port_protocol_cnt:dict)->None:
        with open(self._output_filepath, 'w') as f:
            f.write("Tag Counts:\n")
            f.write("Tag,Count\n")
            for tag, cnt in tag_cnt.items():
                f.write(f"{tag},{cnt}\n")
            f.write("\nPort/Protocol Combination Counts:\n")
            f.write("Port,Protocol,Count\n")
            for (port, protocol), cnt in port_protocol_cnt.items():
                f.write(f"{port},{protocol},{cnt}\n")


def main():
    parser = argparse.ArgumentParser(description="Parse flow logs and generate a report.")

    parser.add_argument('--logs_format', type=str, default='default', help='Specify the flow log format - default or custom.')
    parser.add_argument('--lookup_filepath', type=str, default=LOOKUP_FILEPATH, help='Specify the lookup table filepath.')
    parser.add_argument('--flowlogs_filepath', type=str, default=FLOW_LOG_FILEPATH, help='Specify the flow logs filepath.')
    parser.add_argument('--output_filepath', type=str, default=OUTPUT_FILEPATH, help='Specify the output filepath.')

    args = parser.parse_args()
    lookup_table = LookupTable(LOOKUP_FILEPATH)
    flow_log = FlowLog(log_format=args.logs_format, lookup_table=lookup_table)
    flow_log.parse_logs(args.flowlogs_filepath)
    tag_cnt = flow_log.get_tag_count()
    port_protocol_cnt = flow_log.get_port_protocol_count()
    report_generator = ReportGenerator(args.output_filepath)
    report_generator.generate_report(tag_cnt, port_protocol_cnt)


if __name__ == '__main__':
    main()