import xlrd

# Extracts codes from a spreadsheet file.
# Assumes that the data is in the first collumn with no title.
def extract_codes(filename):
    codes = []
    # open_workbook closes the workbook after loading it into python
    workbook = xlrd.open_workbook(filename)
    sheet_names = workbook.sheet_names()
    if len(sheet_names) > 0:
        worksheet = workbook.sheet_by_name(sheet_names[0])
        if worksheet.ncols > 0:
            for r in range(worksheet.nrows):
                # 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                cell_type = worksheet.cell_type(r, 0)
                # End of the codes
                if cell_type == 0 or cell_type == 6: break
                codes.append(worksheet.cell_value(r, 0))
    return codes
