import openpyxl  # Need this for working with excel docs

def getUnitData(unit, type):

	#Open our workbook and filter to the sheet coresponding to the name of the provided unit
	wb = openpyxl.load_workbook('New Master Test Collection Document.xlsx', data_only=True) #data_only to avoid excel refrences

	try:
		sheet = wb.get_sheet_by_name(unit)
	except Exception, e:
		raise e
	data = []

	#Depending on what data we want to return, either grab the forces or thicknesses
	if type == 'thicknesses':
		for i in range(4, 24, 1):
			data.append(sheet.cell(row=i, column=2).value) #Column 2 is standard for thicknesses

	elif type == 'forces':
		for i in range(4, 24, 1):
			data.append(sheet.cell(row=i, column=9).value) # Column 9 is standard for forces

	else:
		print("Unknown type of unit data %s" %type)

	return data

def getDerekData(length,width,thickness,typeOfSteel,condition,orientation):

	wb = openpyxl.load_workbook('Lifting_Calculations.xlsx', data_only=True)
	sheet = wb.get_sheet_by_name('Sheet Sizes')

	row_indices = []

	for row in sheet.iter_rows(min_row=1, max_col=1, max_row=1025):
		for cell in row:
	        print(cell)

	return 'yes'
