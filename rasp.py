import RPi.GPIO as GPIO
import time
import random
import paho.mqtt.client as paho
import os

#mqtt variables
broker="localhost"
topic = "LED/state"
Ledstate = 0
playerName = input("Enter your player name\n\n") #Store player name

#Set the username and password
username = "mqttuser"
password = "temporarypassword"


#Pin configuration
Button = 16

start = None

#create a random number from 5000 to 10000
ran_num = random.randint(5000,10000)

#indicator to let the program know at what stage the payer is on
game_state = 0

#Funtion that starts the game
def button_time(channel):
    global start, game_state
    #if 0 then the program knows the player hasnt started a game already
    if game_state == 0:
        #player has started the game
        game_state = 1
        #runs shell commeand to insert the kernel module with parameters
        os.system(f"sudo insmod piirq.ko time={ran_num} led_state={Ledstate}")
        #store current time
        start = time.time()
    else:
        #store current time
        end_time = time.time()
        #calculate the time taken and turn it into miliseconds
        elapsed_time = (end_time - start) * 1000
        print(f"Timer stopped. Elapsed time: {elapsed_time:.2f} milliseconds.")
        message = playerName + "," + str(elapsed_time)
        #publish the message to the broker
        publish(client, message)
        #remove the kernel
        os.system("sudo rmmod piirq.ko")
        #game ended
        game_state = 0
        print("Try again for better result!")

#function to check its connected or not and chages the value of led state
def on_connect(client, userdata, flags, rc):
    global Ledstate
    if rc == 0:
        Ledstate = 1
        print("Connected")
    else:
        print(f"Failed {rc}")
        Ledstate = 0
        return
    
#plushing the message function
def publish(client, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Sent")
    else:
        print(f"Failed to send message")

#creates an MQTT Client
client = paho.Client()
client.username_pw_set(username, password)  # Set the username and password
client.on_connect = on_connect
client.connect(broker) #connects to the broker can also put the port number here but the default is 1883
client.loop_start() #loop starts while the code continues to run the next line

GPIO.setwarnings(False) #Ignore warning for now
GPIO.setmode(GPIO.BCM) #Use GPIO mode

#Setups
GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Button onclick events
GPIO.add_event_detect(Button, GPIO.RISING, callback=button_time, bouncetime=500)
message = input("Press enter to quit\n\n") # Run until someone presses enter
#Clean up
GPIO.cleanup() 
client.loop_stop()
