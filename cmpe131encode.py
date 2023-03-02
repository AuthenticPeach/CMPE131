import sys
import csv
import json
import xml.etree.ElementTree as ET

# Read the filename and the desired format from command line arguments
filename = sys.argv[1]
output_format = sys.argv[2]

# Open the file and read the data
with open(filename, 'r') as f:
    data = f.read()

# Convert the data to the desired format
if output_format == '-c':
    # CSV format
    lines = data.split('\n')
    rows = [line.split(',') for line in lines]
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
elif output_format == '-j':
    # JSON format
    rows = [line.split(',') for line in data.split('\n')]
    keys = rows[0]
    values = [dict(zip(keys, row)) for row in rows[1:]]
    with open('output.json', 'w') as f:
        json.dump(values, f)
elif output_format == '-x':
    # XML format
    rows = [line.split(',') for line in data.split('\n')]
    root = ET.Element('data')
    for row in rows:
        item = ET.SubElement(root, 'item')
        for i in range(len(row)):
            key = rows[0][i]
            value = row[i]
            subitem = ET.SubElement(item, key)
            subitem.text = value
    tree = ET.ElementTree(root)
    tree.write('output.xml')

print(f"Converted {filename} to {output_format} format and saved it as output.{output_format}")

