# Flow Log Parsing

## Overview
This script parses a file containing VPC Flow Log data and maps each row to a tag based on a lookup table. The lookup table is defined in a CSV file with three columns: `dstport`, `protocol`, and `tag`. The program uses the combination of `dstport` and `protocol` from the flow log data to determine and apply the appropriate tag from the lookup table.

## Features
- Parses flow log data from a specified file (.csv/.txt/.log).
- Uses a CSV file as a lookup table to map dstport and protocol combinations to tags.
- Supports both default and custom flow log formats.
- Generates reports summarizing tag counts and port/protocol combination counts.
- The output file name includes the date to ensure it doesn't overwrite the previous day's file if this script runs daily. For example, `report_2024-09-14.txt`.
- Handles exceptions like
  - `InvalidFilenameError` if the lookup table or log file doesn't exist.
  - `LookupTableError` if no valid lookup table is provided to the flow log parser.
  - `InvalidLogFormatError` if an unsupported log format is passed via arguments (other than `custom` or `default`).

## Installation

### Pre-requisites
1. Use Python 3.6 or higher.
2. The project uses all default Python packages so no other installations are needed.
3. Ensure that the Lookup Table CSV and Log file are placed under the project folder. Specify the path in the optional arguments while running the script if it differs from the default path.
4. Define the config file.

### Configuration
The project uses a configuration file to manage the constants such as the default filepaths and IANA protocol number mapping. The configuration file `src/config.py` contains the following variables:

`LOOKUP_FILEPATH`: Default path to the CSV file that defines the lookup table for mapping dstport and protocol to tag. Example value: `../data/lookup.csv`.

`FLOW_LOG_FILEPATH`: Default Path to the flow log file that will be parsed. This file should contain flow log data in a format compatible with the specified log format. Example value: `../data/flowlogs.txt`.

`OUTPUT_FILEPATH`: Path where the report file will be saved. The report will include counts of tags and port/protocol combinations. Example value: `../data/output/report.txt`.

`CUSTOM_FLOW_LOG_FIELDS`: List of field names used in custom log format. This is used to identify the index of `dstport` and `protocol` fields. Example value: ['srcaddr', 'dstaddr', 'srcport', 'dstport', 'protocol', 'packets', 'bytes', 'start', 'end', 'action', 'log-status'].

`PROTOCOL_NUMBER_TO_NAME`: Dictionary mapping protocol numbers to their corresponding names. This helps translate numerical protocol values in flow logs to their string representations. Example values:

```bash
{
    1: 'icmp',
    6: 'tcp',
    17: 'udp',
    # Add more mappings here
}
```

### Usage
1. Clone the Repository
```bash
git clone https://github.com/LakshitaBh/Flow-Log-Parsing.git
cd src
```
2. To run the python script with default logs run
```bash
python parse_flow_logs.py
```
To run the python script with custom logs format run
```bash
python parse_flow_logs.py --logs_format=custom
```
The script supports the following optional arguments if custom values are to be used:\
1. `--logs_format`: To specify the flow log format, either default or custom.
2. `--lookup_filepath`: Path to the CSV file containing the lookup table.
3. `--flowlogs_filepath`: Path to the file containing the flow log data.
4. `--output_filepath`: Path where the report file will be saved.

For help with these arguments run
```bash
python parse_flow_logs.py --help
```

## Testing
The code has been tested with log files and lookup files containing spaces, blank lines, and blank files. It handles default log format and custom log formats and gracefully skips or processes invalid entries without crashing. 

## Design Considerations
**Why `config.py` instead of JSON, TOML, or YAML?**
TOML and YAML: These formats would require installing non-default Python packages.
JSON: Although it's a widely-used configuration format, JSON can be tricky to modify and easily introduce errors such as missing brackets.

## Improvements
If the flow log file size and the lookup file size are large, we can introduce asynchronous programming to process multiple rows in parallel using `asyncio`.

### References
https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html \
https://docs.python.org/3/library/asyncio.html
