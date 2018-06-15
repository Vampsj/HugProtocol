#!/usr/bin/python
import MySQLdb
import mysql.connector
import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

src_uid = 1111111111111111
# Server address
mysql_host = "mysql1.php.xdomain.ne.jp"
# MySql username and password
mysql_user = "satosugar_sato"
mysql_pwd = "tsukuba2018"
mysql_db = "satosugar_hagprotocol"
mysql_table = "authenticate"
uid_list = []



def insert_data_2 (host, user, pwd, db):
    mydb = mysql.connector.connect(host, user, pwd, db)

    mycursor = mydb.cursor()

    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = ("John", "Highway 21")
    mycursor.execute(sql, val)

    mydb.commit()
}
print(mycursor.rowsaffected, "record inserted.")



def change_to_num(target):
    result = 0
    itera = 0
    for i in target:
        result = result + i * pow(10, itera)
        itera = itera + 1
    return result

# Open database connection
def insert_data(host, user, pwd, sdb, src_id, des_id):
    print "try to connect"
    db = MySQLdb.connect(host, user, pwd, sdb)
    print "connected"
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    # Example
    sql = "INSERT INTO authenticate(src, des) VALUES ('%d', '%d')" %(src_id, des_id)
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database

       print "Successfully insert into database!"
    except:
       # Rollback in case there is any error
       db.rollback()

       # disconnect from server
       db.close()

# Capture SIGINT for cleanup when the script is aborted and insert obtained uid to database
def end_read(signal,nframe):
    global continue_reading
    print "Contacts added and end reading."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the HugProtocol"
print "Press Ctrl-C to stop."


while continue_reading:
    if not len(uid_list) == 0:
        print len(uid_list)
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            user_id = MIFAREReader.MFRC522_Return_Data(8)
            print user_id
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

        # Use UID as key of the dict
        # However in fact, we want the real user id rather than tag's uid
        if not user_id in uid_list:
            user_id = change_to_num(user_id)
            print user_id
            uid_list.append(user_id)
            print "\n inserting data"
            insert_data(mysql_host, mysql_user, mysql_pwd, mysql_db, src_uid, user_id)

        # Don't know whether its needed
        '''# This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"'''
