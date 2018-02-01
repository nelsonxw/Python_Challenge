import csv, os

def import_data(filename):
    """pass users entered file names to avoid future maintenance work of updating file names in the code
    if incorrect names are entered, allow users to re-enter or quit from the program"""

    # assuming data files are saved in a sub folder called 'data folder' under the same directory
    # create an indirect path to feed into file open function
    path = os.path.join('data folder', filename)
    try:
    # when filename is valid and found, read the lines from source file and write into vote.csv file
        with open('vote.csv', 'a', newline='') as csvfile:
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

# delete old vote.csv file, if any, so that it will not append new data to old data from previous executions
if os.path.exists('vote.csv'):
    os.remove('vote.csv')

# create a blank csv file with headers only
with open('vote.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Voter ID', 'County', 'Candidate'])

# ask users to enter the file name of election source data
filename = input('Please enter the file name of election data, including file extensions like csv -> ')
import_data(filename)

Add_more_data = True

# if there are more than one source data file, allow users to append more files to create a consolidated file
while Add_more_data == True:
    user_response = input('Do you have additional data to import? Y(es) or N(o) -> ')
    if user_response == 'Y':
        filename = input('Please enter the file name of election data, including file extensions like csv -> ')
        import_data(filename)
    elif user_response == 'N':
        Add_more_data = False
    else:
        print('Invalid answer.  Please try again! ')

# create a dictionary 'candidate_count' to count the votes by candidate
candidate_count = {}

# count votes and identify the winner
with open('vote.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # skip the header line
    next(reader, None)
    for row in reader:
        # if candidate name not in the candidate count file, add the name to the count file and add 1 to vote count
        if row[2] not in candidate_count.keys():
            candidate_count[row[2]] = 1
        # if candidate name already in the count file, add 1 to the vote count
        else:
            candidate_count[row[2]] += 1

    # calculate the total count in the election
    total_vote = (sum(candidate_count.values()))

    vote = 0
    winner = ''
    # find out which candidate has most of the votes
    for line in candidate_count.keys():
        if candidate_count[line] > vote:
            vote = candidate_count[line]
            winner = line

# save vote results to txt file in the format required
with open('vote_results.txt','w') as txtfile:
    txtfile.writelines('Election Results\n' + '-' * 25 + '\n')
    txtfile.writelines(['Total Votes: ', str(total_vote)])
    txtfile.writelines('\n' + '-' * 25 + '\n')

    for line in candidate_count.keys():
        txtfile.writelines([line + ': ', str('{:.1%}'.format(candidate_count[line] / total_vote)),
                            ' (' + str(candidate_count[line]) + ')' + '\n'])

    txtfile.writelines('\n' + '-' * 25 + '\n')
    txtfile.writelines(['Winner: ',winner])
    txtfile.writelines('\n' + '-' * 25 + '\n')

# print out vote results to screen
with open('vote_results.txt','r') as txtfile:
    for line in txtfile:
        print(line.rstrip())