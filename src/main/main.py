import csv
import sqlite3

# Connect to a local SQLite database file
conn = sqlite3.connect('callcenter.db')

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
    load_and_clean_users('resources/users.csv')
    load_and_clean_call_logs('resources/callLogs.csv')
    write_user_analytics('resources/userAnalytics.csv')
    write_ordered_calls('resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Save changes, then close the cursor and connection. main function ends here.
    conn.commit()
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    """I created an array to hold the name i loops through the csv file if 
    the len of the word isnt equal to two we skip over it if its good we put it into our array. """

    filter_names = []
    with open(file_path, "r") as l:
        for line in l:
            words = line.split(",")
            if len(words) != 2:
                continue

            if words[0].strip() == "" or words[1].strip() == "":
                continue

            if words[0].strip() == "firstName" and words[1].strip() == "lastName":
                continue

            first_name = words[0].strip()
            last_name = words[1].strip()

            filter_names.append([first_name, last_name])
            

    cursor.executemany("""
        INSERT INTO USERS (firstName, lastName)
        VALUES(?,?)
        """, filter_names)
    

    cursor.execute(
        """
        SELECT * 
        FROM users 
        """
    )
    rows = cursor.fetchall()
    print(rows)


            
            


    print("TODO: load_users")


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):

    clean_log = []

    with open(file_path, 'r') as fl:
        for line in fl:
            log = line.split(",")
            
            if len(log) != 5:
                continue

            if log[0].strip() == "" or log[1].strip() == "" or log[2].strip() == "" or log[3].strip() == "" or log[4].strip() == "" :
                continue

            if log[0].strip() == "phoneNumber":
                continue

            log1 = log[0].strip()
            log2 = log[1].strip()
            log3 = log[2].strip()
            log4 = log[3].strip()
            log5 = log[4].strip()
            clean_log.append([log1,log2,log3,log4, log5])



    cursor.executemany(
    """
    INSERT INTO callLogs (
        phoneNumber,
        startTime,
        endTime,
        direction,
        userId
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    clean_log
)

    cursor.execute(
        """
        SELECT * 
        FROM callLogs
        """
    )
    #rows = cursor.fetchall()
    # print(rows)



# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):

    cursor.execute("""
                SELECT callLogs.userId, AVG(endTime- startTime) AS avgDuration, COUNT(*) AS numCalls
                FROM callLogs
                LEFT JOIN users
                    ON callLogs.userId = users.userId
                GROUP BY callLogs.userId""")
    
    rows = cursor.fetchall()
    print(rows)

    with open(csv_file_path, 'w') as fl:
        writer = csv.writer(fl)
        writer.writerow(["userId", "avgDuration", "numCalls"])
        writer.writerows(rows)



# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):

    cursor.execute("""
                SELECT * 
                FROM `callLogs`
                ORDER BY `userId`, `startTime` """)
    
    rows = cursor.fetchall()

    with open(csv_file_path, 'w') as fl:
        writer = csv.writer(fl)
        writer.writerow(["callId","phoneNumber","startTime","endTime","direction","userId"])

        writer.writerows(rows)


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



#python3 src/main/main.py
