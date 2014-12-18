import xlrd, csv, os

# Parses files uploaded to the server
# Intended to be used to read a single collumn of a spreadsheet, csv, or
# lines of text.
#
# Example
# values = FileParser(filename).extract_values()

class FileParser():
    @staticmethod
    def extension(filename):
        name, extension = os.path.splitext(filename)
        return extension

    @staticmethod
    def parse_txt(filename):
        with open(filename, 'r') as f:
            return [line.rstrip() for line in f]

    @staticmethod
    def parse_csv(filename):
        values = []
        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
            values = [row[0] for row in reader]
        return values

    @staticmethod
    def parse_spreadsheet(filename):
        values = []
        # open_workbook closes the workbook after loading it into python
        workbook = xlrd.open_workbook(filename)
        sheet_names = workbook.sheet_names()
        if len(sheet_names) > 0:
            worksheet = workbook.sheet_by_name(sheet_names[0])
            if worksheet.ncols > 0:
                for r in range(worksheet.nrows):
                    # 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_type = worksheet.cell_type(r, 0)
                    # End of the values
                    if cell_type == 0 or cell_type == 6: break
                    values.append(worksheet.cell_value(r, 0))
        # Maintain behavior across all parsers
        # Codes needn't be univalue
        values = [value.encode('ascii', 'ignore') for value in values]
        return values
        return extension

    def __init__(self, filename):
        self.filename = filename

    def extract_values(self):
        PARSERS = {
            ".xlsx": FileParser.parse_spreadsheet,
            ".xls":  FileParser.parse_spreadsheet,
            ".txt":  FileParser.parse_txt,
            ".csv":  FileParser.parse_csv
        }
        parser = PARSERS[FileParser.extension(self.filename)]
        values = parser(self.filename)
        # TODO(seanraff): Fancy handling of headers
        return values
