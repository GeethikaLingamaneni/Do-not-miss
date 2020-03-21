

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import smtplib
import time
import subprocess
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import RPi.GPIO as GPIO

import urllib2
import cookielib
from getpass import getpass
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

client=mqtt.Client()
client.connect('iot.eclipse.org',1883)
print('Client Connected to Subscriber')


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Define GPIO to use on
GPIO_TRIGGER = 15
GPIO_ECHO    = 11

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)
time.sleep(0.5)

# Send 10us pulse to trigger
GPIO.output(GPIO_TRIGGER, True)
time.sleep(0.00001)
GPIO.output(GPIO_TRIGGER, False)


while GPIO.input(GPIO_ECHO)==0:
  start = time.time()

while GPIO.input(GPIO_ECHO)==1:
  stop = time.time()

# Calculate pulse length
elapsed = stop-start

# Distance pulse travelled in that time is time
# multiplied by the speed of sound (cm/s)
distance = elapsed * 34300

# That was the distance there and back so halve the value
distance = distance / 2

print'distance=%.1f'%distance

if distance <=10:

#message
  username = "9553181381"
  passwd = "swaroop95531"
  message = "someone is near to me at distance of %.1f" %distance
  number = "9553181381"
  message = "+".join(message.split(' '))
  print "entered to send sms" 
#Logging into the SMS Site
  url = 'http://site24.way2sms.com/Login1.action?'
  data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
 
#For Cookies:
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
 
# Adding Header detail:
  opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')]
 
  try:
    usock = opener.open(url, data)
  except IOError:
    print "Error while logging in."
    sys.exit(1)
    

 
  jession_id = str(cj).split('~')[1].split(' ')[0]
  send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
  send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
  opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
 
  try:
    sms_sent_page = opener.open(send_sms_url,send_sms_data)
  except IOError:
    print "Error while sending message"
    

    print "SMS has been sent."

# Reset GPIO settings


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print('Received From : '+msg.topic)
    print('Received Msg : '+str(msg.payload))
    '''t=msg.topic
    print(t)
    publishmessage(t,'THanks For your input')'''
    

  

    if((msg.payload)=="open"):
        GPIO.output(16,True)        
        GPIO.output(18,False)
        print "Motor on"
        time.sleep(10)
        GPIO.output(16,False)        
        GPIO.output(18,False)
        strFrom = 'pswaroop000@gmail.com'
        strTo = 'pswaroop000@gmail.com'

#create email
#camera        
# Create the root message and fill in the from, to, and subj$
        msgRoot = MIMEMultipart()
        msgRoot['Subject'] = 'subject'
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo


        
        GPIO.setup(7, GPIO.IN)
        print "press button to send email"
        for i in range(2):
          input=GPIO.input(7)
          if input == False:
                print "button pressed"
                subprocess.Popen(["fswebcam","-r 640x480", "capture.jpg"])
                #time.sleep(2)
                # This example assumes the image is in the current
                # directory
                fp = open('capture.jpg','rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                msgRoot.attach(msgImage)
                # send mail
                s = smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login('pswaroop000@gmail.com' , 'swaroop9553')
                s.sendmail(strFrom, strTo,msgRoot.as_string())
                s.close()
                print "Email sent"
                time.sleep(3)

    elif((msg.payload)=="close"):
        GPIO.output(16,False)        
        GPIO.output(18,True)
        print "Motor off"
        time.sleep(10)
        GPIO.output(16,False)        
        GPIO.output(18,False)
        strFrom = 'pswaroop000@gmail.com'
        strTo = 'pswaroop000@gmail.com'

#create email
#camera        
# Create the root message and fill in the from, to, and subj$
        msgRoot = MIMEMultipart()
        msgRoot['Subject'] = 'subject'
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo


        
        GPIO.setup(7, GPIO.IN)
        print "press button to send email"
        for i in range(2):
          input=GPIO.input(7)
          if input == False:
                print "button pressed"
                subprocess.Popen(["fswebcam","-r 640x480", "capture.jpg"])
                #time.sleep(2)
                # This example assumes the image is in the current
                # directory
                fp = open('capture.jpg','rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                msgRoot.attach(msgImage)
                # send mail
                s = smtplib.SMTP('smtp.gmail.com',587)
                s.starttls()
                s.login('pswaroop000@gmail.com' , 'swaroop9553')
                s.sendmail(strFrom, strTo,msgRoot.as_string())
                s.close()
                print "Email sent"
                time.sleep(3)
    
def publishmessage(token,msg):
    client.publish(token,msg)
      

def read_msg(stoken):
    client.subscribe(stoken)
    
    client.on_message = on_message
    client.loop_forever()

publishmessage('swaroop','HI from surya')
read_msg('swaroop')
GPIO.cleanup()
# sudo pip install flask
#sudo pip install paho-mqtt


    
