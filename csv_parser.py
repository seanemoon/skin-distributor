import csv

def extract_codes(filename):
    codes = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        codes = [row[0] for row in reader]
    return codes
