def extract_codes(filename):
    with open(filename, 'r') as f:
        return [line.rstrip() for line in f]
