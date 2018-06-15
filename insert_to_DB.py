#!/usr/bin/python
import requests
import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# source user id
src_uid = 1
# Server address
url = "http://satosugar.php.xdomain.jp/db_write_authenticate.php"
# targed user id list
uid_list = []


def change_to_num(target):
    target = target[::-1]
    result = 0
    itera = 0
    for i in target:
        result = result + i * pow(10, itera)
        itera = itera + 1
    return int(result)


def insert_data(src_id, des_id):
    print(uid_list)
    if src_id == des_id:
        return

    r = requests.get(url, params= {"src":src_id, "des":des_id})
    print "inserted"
    
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
            des_uid = MIFAREReader.MFRC522_Return_Data(8)
            print des_uid
            MIFAREReader.MFRC522_StopCrypto1()

            # Use UID as key of the dict
            # However in fact, we want the real user id rather than tag's uid
            print(uid_list)
            des_uid = change_to_num(des_uid)
            if des_uid in uid_list:
                print "Already in list."
            else:
                uid_list.append(des_uid)
                print "\n inserting data"
                insert_data(src_uid, des_uid)
        else:
            print "Authentication error"

        
