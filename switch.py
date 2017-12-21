## Ian, this was written in python 2.7. Hope this helps...

#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
import os, sys
import serial
import smtplib
import time

## Creates log file
logging.basicConfig(filename='switchlog.txt', level=logging.INFO)


    ## Console commands for switching the maplin's wifi plug, please check that the channel is correct,
    ## otherwise change the below line for the channel and button required.
    ## PLEASE REFER TO THIS TUTORIAL IF YOU HAVE ANY QUESTIONS
    ## https://riviera.org.uk/2015/01/15/using-a-raspberry-pi-to-control-maplin-power-sockets/

def turnPlugON():
    ON = 'sudo ~/raspberry-strogonanoff/src/strogonanoff_sender.py --channel 1 --button 1 --gpio 0 on'
    os.system(ON)

def turnPlugOFF():
    OFF = 'sudo ~/raspberry-strogonanoff/src/strogonanoff_sender.py --channel 1 --button 1 --gpio 0 off'
    os.system(OFF)
    logging.info(logTimestamp())
    logging.info("The plug is off.\n")
    sendLogToEngineering()
    time.sleep(1)
    quit()

def logTimestamp():
    """
    Creates a timestamp for a log in YYYY-Mmm-DD(Ddd), HH:MM:SS MS format

    Refer to https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    """
    return datetime.datetime.now().strftime('%Y-%b-%d(%a), %H:%M:%S %f')

def startingProcedure():
    logging.info(logTimestamp())
    logging.info("Hi there, I'm Switch! Please bear with me, while I'm checking my stuff.\n")
    time.sleep(1)
    logging.info(logTimestamp())
    logging.info("Testing\n")
    time.sleep(2)
    logging.info(logTimestamp())
    logging.info("Switching on...\n")
    turnPlugON()
    time.sleep(2)
    turnPlugON()

def sendLogToEngineering():
    """
    This function sends an email with a log to engineering inbox.
    Name: Raspberry Pi
    Surname: W____ F___
    Birthday: September 5, 1917 (because google doesn't allow me to choose 2017, which is today)
    Gender: Rather not say
    Mobile: +44__________

    Please try not to change anything, it was taken from
    https://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector
    """
    TO = 'V________@_______.com'
    GMAIL_USER = '________.raspberrypi@gmail.com'
    GMAIL_PASS = 'iam________raspberrypi'

    SUBJECT = 'SENSOR TRIGGERED'
    line1 = 'This is an automated email. This message means either of two things:\n'
    line2 = 'Liquid has been detected and motor has been shut down. Please visit the site immediately to confirm.\n'
    line3 = 'or\n'
    line4 = 'An error in the script has occured.\n'
    line5 = 'Either way, please get to the premises ASAP. \n CHECK LOGS FOR DETAILS.'

    logging.info(logTimestamp())
    logging.info("Sending email to Engineering\n")

    log = ''

    file = open("switchlog.txt", "r")
    for line in file:
        log += line
    file.close()

    TEXT = line1+line2+line3+line4+line5 + 3*"\n" + log

    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT + '\n'
    print header
    msg = header + '\n' + TEXT + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, TO, msg)
    smtpserver.close()

try:
    startingProcedure()
except Exception:
    logging.info(logTimestamp())
    logging.info("There is problem with startingProcedure function. Check it!\n")
    turnPlugOFF()
try:
    ##  Connecting arduino board. Ammend port name below if required.
    ##  For details see: https://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector
    ser = serial.Serial('/dev/ttyACM0', 9600)
except Exception:
##  If this error happens, go to Arduino IDE and in "Tools" tab check, whether the connection name
##  and port name match.
    logging.info(logTimestamp())
    logging.info("Problem with arduino connection. Check the port connection config!\n")
    turnPlugOFF()

logging.info(logTimestamp())
logging.info("I think we are good to go.\n")

while True:
    message = ser.readline()
    ##  Check whether liquid is present
    if message[0] == "1":
        logging.info(logTimestamp())
        logging.info("Liquid detected, verifying...\n")
        time.sleep(3)
        message = ser.readline()
##      Check again in case someone just holds it in their hand
        if message[0] == "1":
            logging.info(logTimestamp())
            logging.info("Liquid presence confirmed. Shutting down the plug.\n")
            turnPlugOFF()
        else:
            logging.info(logTimestamp())
            logging.info("Liquid presence unverified.\n")
    time.sleep(1)
