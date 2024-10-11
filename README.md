# VPC-Flow-Logs-Parser

# Flow Log Parser Project

This project parses flow log data and maps each row to a tag based on a lookup table (CSV). The flow logs are read from the data/flow_logs.txt file, and the lookup table is located in data/lookup_table.csv. The output is written to a file called output_report.txt, showing tag counts and port/protocol combination counts.

The files lookup_table.csv and flow_logs.txt were custom generated, with the flow logs following Version 2 of VPC flow log records and adhering to the default format for version 2 logs.

# Prerequisites

1. Python 3.x should be installed on your machine.
2. The input files flow_logs.txt and lookup_table.csv should be present in the data/ directory.

# How to Run the Project
1. Clone or download this repository and navigate to the flow_log_parser_project directory.
2. Ensure you have Python 3.x installed. You can check your Python version by running:
   
   python --version 
4. Run the script:
   
   python3 flow_log_parser.py
6. Output:
   
   The output of the program will be saved in output_report.txt, which will include:
   Tag counts based on the dstport and protocol combination.
   Port and protocol combination counts.
