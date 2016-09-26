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

def getDerekData(thickness, width, length, typeOfSteel, condition,orientation):

	wb = openpyxl.load_workbook('Lifting_Calculations.xlsx', data_only=True)
	sheet = wb.get_sheet_by_name('Sheet Sizes')

	row_indices = []

	for row in sheet.iter_rows(min_row=1, max_col=18, max_row=1025):
		name = str(row[0].value)
		searchString = "%s\"%s\'%s\'" %(thickness, width, length)
		if (searchString in name) & (row[17].value == 'Yes'):
			for item in row:
				print(item.value)

	return {"PlateWeight":row[6].value,"SWLperMag":int(row[8].value)/4, "SafteyFactor":row[10].value}
