import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('D:\\revature\\pkgupta28-pep-pythonSQL-project\\src\\test\\testUsers.csv')
    load_and_clean_call_logs('D:\\revature\\pkgupta28-pep-pythonSQL-project\\src\\test\\testCallLogs.csv')
    write_user_analytics('D:\\revature\\pkgupta28-pep-pythonSQL-project\\src\\test\\testUserAnalytics.csv')
    write_ordered_calls('D:\\revature\\pkgupta28-pep-pythonSQL-project\\src\\test\\testOrderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
     with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        
        next(reader, None)
        
        for row in reader:
            
            if len(row) != 2:
                continue 
            
            first_name = row[0].strip()
            last_name = row[1].strip()
            
            if first_name and last_name:
                cursor.execute('''
                    INSERT INTO users (firstName, lastName) VALUES (?, ?)
                ''', (first_name, last_name))
        conn.commit()


        print("TODO: load_and_clean_users")
           


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)    
        for row in reader:
            if len(row) != 5:  
                continue
            
            phoneNumber, startTime, endTime, direction, userId = row
            
           
            if phoneNumber and startTime and endTime and direction and userId:
                cursor.execute('''
                    INSERT INTO callLogs (phoneNumber, startTime, endTime, direction, userId)
                    VALUES (?, ?, ?, ?, ?)
                ''', (phoneNumber, startTime, endTime, direction, userId))
                
    
    conn.commit()


    print("TODO: load_call_logs")


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    user_analytics = {}
    cursor.execute('SELECT userId, startTime, endTime FROM callLogs')
    call_logs = cursor.fetchall()

    for row in call_logs:
        userId, startTime, endTime = row
        
        call_duration = int(endTime) - int(startTime)
        if userId in user_analytics:
            user_analytics[userId]['total_duration'] += call_duration
            user_analytics[userId]['num_calls'] += 1
        else:
            user_analytics[userId] = {'total_duration': call_duration, 'num_calls': 1}
    for userId, analytics in user_analytics.items():
        avg_duration = analytics['total_duration'] / analytics['num_calls']
        user_analytics[userId] = {'avg_duration': avg_duration, 'num_calls': analytics['num_calls']}
    
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['userId', 'avgDuration', 'numCalls']) 
        
        for userId, analytics in user_analytics.items():
            writer.writerow([userId, analytics['avg_duration'], analytics['num_calls']])

    print("TODO: write_user_analytics")


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):
    cursor.execute('SELECT * FROM callLogs ORDER BY userId, startTime')
    call_logs = cursor.fetchall()
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['phoneNumber', 'startTime', 'endTime', 'direction', 'userId'])  
        
        for row in call_logs:
            writer.writerow(row)

    print("TODO: write_ordered_calls")



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()
