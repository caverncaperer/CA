'''
CA.PY
Reads output from M$ certutil command and produces an
'approximately' CSV formatted document
'''

import re
import argparse
import sys

if len(sys.argv) != 2:
    sys.exit("An input filename is required")

print sys.argv[1]

# Constants
column_names = ("requester name:", "issued common name:", "issued email address:",
                 "issued organization unit:", "certificate effective date:","certificate expiration date:")
consts_size = len(column_names)

#source_file = "/home/bitnami/Dropbox/backup/code/python/ca/ca.txt"
#source_file = "/users/ralfey/Dropbox/backup/code/python/ca/ca.txt"

# Set the source and output filenames
#source_file = "/home/bitnami/Dropbox/backup/code/python/ca/defaultuser_080212.txt"

#source_file = "/home/ralfey/Dropbox/backup/code/python/ca/defaultuser_080212.txt"
source_file = sys.argv[1]

outfile = "./certs.txt"

# Open the source file and read into a list
file = open(source_file,'r')
lines = file.readlines()
# Add a null character to the end of the list so the final entry gets processed, don't ask why
lines.append("")

# print lines

# Put together a regex for the header format we are looking for - 'row xxxxx'
# This value could be anything where the source document is formatted as:
#
# 'Row'
#    'string1'
#    'string2'
#    '....'

row_find = re.compile(('row [0-9]{1,3}|[1-4][0-9]{3}|5000'))

# Get the size of the file in terms of lines
total_lines = len(lines)
# print total_lines

# Create an empty list to use for holding the content of each header
combined_row = []
new_row = ""
row_count = 0
fi = 0

# Enumerate through the list and include an iterator for the position in the list
for pos, each in enumerate(lines):
    # Retrieve the element and match the regex against it
    each = each.strip().lower()
    row = re.match(row_find, each)
        
    # Check for a matching line, i.e. one that includes the row xxxx header
    if row <> None:
        # Get the length of each matching line
        row_len = len(each)
                
        # Continue whilst the line is not blank and the position of the list
        # is less than the total items in the list
        while each <> "" and fi < total_lines:
            fi = pos
            found_row = ""
            # print "Match found at element %d\n" % pos
            
            # Retrieve the elements from the list, those beneath the header
            for f in lines:
                if fi <= total_lines:
                    # Remove all leading and trailing spaces and change case
                    found_row = lines[fi].rstrip().lstrip().lower()
                else:
                    break
                
                # Get the length of the row
                found_len = len(found_row)
                
                # Now loop though the list of row prefixes
                for r in column_names:
                    # Get the length of the row prefix to search for
                    cols_found_len = len(r)
                    # Extract the row prefix from the actual found row
                    found_row_column = found_row[:cols_found_len]
                    # Search for the row prefix in the actual row itself
                    cols_found = r.find(found_row_column)
                    # print found_row, cols_found, cols_found_len
                    # If the the find method returns a value other than -1
                    if cols_found >= 0:
                        #new_col = r[cols_found:(cols_found_len+1)]
                        # Remove the column prefix from the row 
                        found_row = found_row[(cols_found_len+1):]
                        #print found_row
                        # We don't need to complete the iteration through the row prefixes so ...
                        break
                    
                # Append each element from the row processed to form a single string
                new_row = (new_row + found_row + ",")
                
                # Look for a blank element from this list which indicates
                # the end of the section
                if found_row == "":
                    # row_count = row_count +1
                    # print  "%d" % found_len
                    # Add the new combined single string to the output list
                    combined_row.append(new_row)
                    new_row = ""
                    row_count = row_count +1
                
                # Increment the position indicator
                fi = (fi + 1)
                # print fi
                # print combined_row
                # print fi,total_lines
                                
    break

# Open the file for output
output = open(outfile,'w+')    

# Output the list to the file including appending a newline
for item in combined_row:  
  output.write("%s\n" % item)