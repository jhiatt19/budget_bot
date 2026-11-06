import csv
import json
from datetime import datetime
from pathlib import Path

def clean_row(row):
    if row['Posting Date']:
        row['Posting Date'] = datetime.strptime(row['Posting Date'], "%m/%d/%Y").strftime("%Y-%m-%d")
    if row['Amount']:
        print(row['Amount'])
        row['Amount'] = row['Amount'][1:]
    return row

def main(file,output):
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        data = [clean_row(row) for row in csv_reader]

    with open(output, mode='w', encoding='utf-8',) as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    file = Path(input("Enter file name: "))
    output = 'transactions' + str(datetime.today())[:10] + '.json'
    main(file,output)
