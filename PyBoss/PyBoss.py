import csv, os, datetime

def import_data(filename):
    """pass users entered file names to avoid future maintenance work of updating file names in the code
    if incorrect names are entered, allow users to re-enter or quit from the program"""

    # assuming data files are saved in a sub folder called 'data folder' under the same directory
    # create an indirect path to feed into file open function
    path = os.path.join('data folder', filename)
    try:
    # when filename is valid and found, read the lines from source file and write into original_records.csv file
        with open('original_records.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            source_data = csv.reader(open(path, 'r', newline=''))
            next(source_data,None)
            for row in source_data:
                writer.writerow(row)
    # if filename is incorrect or not found, give users options to quit or try again
    except OSError:
        response = input('File not found!.  Please try again or enter \'quit\' to exit.')
        if response == 'quit':
            raise SystemExit
        else:
            import_data(response)

# delete old original_records.csv file, if any, so that it will not append new data to old data from previous executions
if os.path.exists('original_records.csv'):
    os.remove('original_records.csv')

# create a blank csv file with headers only
with open('original_records.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Emp ID', 'Name', 'DOB','SSN','State'])

# ask users to enter the file name of employee data
filename = input('Please enter the file name of employee data, including file extensions like csv -> ')
import_data(filename)

Add_more_data = True

# if there are more than one source data file, allow users to append more files to create a consolidated file
while Add_more_data == True:
    user_response = input('Do you have additional data to import? Y(es) or N(o) -> ')
    if user_response == 'Y':
        filename = input('Please enter the file name of employee data, including file extensions like csv -> ')
        import_data(filename)
    elif user_response == 'N':
        Add_more_data = False
    else:
        print('Invalid answer.  Please try again! ')

# define a dictionary to look up the two-letter abbreviation of a state
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# copy original data to a different file 'updates.csv', and modify data per requirements in the new file
with open('updates.csv', 'w', newline='') as update_file:
    writer = csv.writer(update_file, delimiter=',')

    with open('original_records.csv','r',newline='') as input_file:
        reader = csv.reader(input_file,delimiter=',')
        # get the header from the original records file for passing to the new file
        headers = next(reader,None)
        # create the header in the new file
        writer.writerow(headers + ['First Nmae','Last Name','DOB','State'])

        for row in reader:
            # split name to first name and last name
            fn = row[1].split()[0]
            ln = row[1].split()[1]
            # hide the first 5 digits in the SSN
            row[3] = '***-**-' + row[3][-4:]
            # change the date format in the birthday column per the requirement
            new_DOB = datetime.datetime.strptime(row[2],'%Y-%m-%d').strftime('%m/%d/%Y')
            # look up the two-letter abbreviation of state names
            new_state = us_state_abbrev[row[4]]
            # copy data from the original data file and add new modified data
            writer.writerow(row + [fn, ln,new_DOB,new_state])

# select the appropriate columns from the updates file and save to final result file 'updated_records'
with open('updated_records.csv','w',newline='') as output_file:
    writer = csv.writer(output_file,delimiter=',')
    with open('updates.csv','r',newline='') as updates:
        reader = csv.reader(updates,delimiter=',')
        for row in reader:
            writer.writerow([row[0],row[5],row[6],row[7],row[3],row[-1]])

# print out the results to the terminal
with open('updated_records.csv', 'r', newline='') as output_file:
    writer = csv.reader(output_file, delimiter=',')
    for line in writer:
        print(line)


