# Converts a Microsoft Excel 2007+ file into plain text (Includes VBA Code)
# for comparison using git diff
#
# Instructions for setup:
# 1. Place this file in a folder
# 2. Add the following line to the global .gitconfig:
#    -use cmd way as not to corrupt file
#	 [diff "zip"]
#   	binary = True
#		textconv = python c:/path/to/git_diff_xlsm.py
#
# CMD Way: git config --global diff.zip.textconv "python c:/path/to/git_diff_xlsm.py"
#3. Add OfficeMalScanner.exe to /path/to/ directory where this script is
# 4. Add the following line to the repository's .gitattributes
#	*.xlsm diff=zip
# 5. Now, typing [git diff] at the prompt will produce text versions
# of Excel .xlsm files


# may need to pip install xlrd

import sys
import os
import shutil
import zipfile,os.path
import xlrd as xl

def unzip(source_filename, dest_dir):
	with zipfile.ZipFile(source_filename) as zf:
		for member in zf.infolist():
			# Path traversal defense copied from
			# http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
			words = member.filename.split('/')
			path = dest_dir
			for word in words[:-1]:
				drive, word = os.path.splitdrive(word)
				head, word = os.path.split(word)
				if word in (os.curdir, os.pardir, ''): continue
				path = os.path.join(path, word)
			zf.extract(member, path)


def parse(infile,outfile):
	"""
	Converts an Excel file's VBA Macro code into text
	Returns a formatted text file for comparison using git diff.
	"""
	#change .xlsm to zip
	shutil.copyfile(infile, os.getcwd() +"\\tempfile.zip")
	#unzip the .xlsm file
	unzip("tempfile.zip", os.getcwd() + "\\temp")
	#run OfficeMalScanner.exe on vbaproject.bin from xlsm to get VBA code
	os.system("OfficeMalScanner.exe " + os.getcwd() + "\\temp\\xl\\xl\\vbaProject.bin info")

	#Parse VBA Code
	path = os.getcwd() + "\\VBAPROJECT.BIN-Macros"  # remove the trailing '\'
	data = {}
	for dir_entry in os.listdir(path):
		dir_entry_path = os.path.join(path, dir_entry)
		if os.path.isfile(dir_entry_path):
			with open(dir_entry_path, 'r') as my_file:
				outfile.write("=================================\n")
				outfile.write("Sheet VBA Code: " + dir_entry + "\n")
				outfile.write("=================================\n")
				outfile.write(my_file.read())

def parseSheet(infile,outfile):
	"""
	Taken From: https://github.com/willu47/git_diff_xlsx/blob/master/git_diff_xlsx.py

	Converts an Excel file into text
	Returns a formatted text file for comparison using git diff.
	"""

	book = xl.open_workbook(infile)

	num_sheets = book.nsheets

	print( book.sheet_names())

#   print "File last edited by " + book.user_name + "\n"
	outfile.write("File last edited by " + book.user_name + "\n")

	def get_cells(sheet, rowx, colx):
		return sheet.cell_value(rowx, colx)

	# loop over worksheets

	for index in range(0,num_sheets):
		# find non empty cells
		sheet = book.sheet_by_index(index)
		outfile.write("=================================\n")
		outfile.write("Sheet: " + sheet.name + "[ " + str(sheet.nrows) + " , " + str(sheet.ncols) + " ]\n")
		outfile.write("=================================\n")
		for row in range(0,sheet.nrows):
			for col in range(0,sheet.ncols):
				content = get_cells(sheet, row, col)
				if content != "":
					outfile.write("	" + str(xl.cellname(row,col)) + ": " + str(content) + "\n")
		print( "\n")

##def cleanUp():

# output cell address and contents of cell
def main():
	args = sys.argv[1:]
	if len(args) != 1:
		print('usage: python git_diff_xlsx.py infile.xlsx')
		sys.exit(-1)
	outfile = sys.stdout
	parse(args[0],outfile)
	print("\n \n")
	parseSheet(args[0],outfile)

if __name__ == '__main__':
	main()
