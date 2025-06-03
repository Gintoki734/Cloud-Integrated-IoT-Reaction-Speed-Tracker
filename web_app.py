import boto3
from flask import Flask, render_template
import paho.mqtt.client as paho
from decimal import Decimal

# Variables for MQTT
broker = "3.224.212.44"
PlayerName = ""
ResponseTime = 0

app = Flask(__name__)

#Create a session
session = boto3.session.Session()

#Connect to DynamoDB 
dynamodb = session.resource('dynamodb', region_name='us-east-1')
#the table where the data will be stored on
table = dynamodb.Table('ButtonDB')

#function to insert the variables in the database
def insert():
    try:
        response = table.put_item(
            Item={
                "Game_Name": "Button_Game",
                "Response_Time": ResponseTime,
                "Player_Name": PlayerName
            }
        )
        print(f"Item inserted: {response}")
    except Exception as e:
        print(f"Error inserting item: {e}")

#query the database to get 10 lowest numbers
def get_top_scores():
    sorted_items = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('Game_Name').eq('Button_Game'),
        ScanIndexForward=True,
        Limit=10,
        ProjectionExpression="Player_Name, Response_Time"
    )
    return sorted_items.get('Items', [])

#function to check if MQTT connected or not
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
    else:
        print(f"Failed {rc}")

#function that gets trigged when MQTT receives the message
def received_msg(client, userdata, msg):
    global PlayerName, ResponseTime, scal
    #data is splitted and stoped in the global variable
    PlayerName, ResponseTime = msg.payload.decode("utf-8").split(",")
    ResponseTime = Decimal(ResponseTime)
    insert()  #Insert new data into DynamoDB
    scal = get_top_scores()  #Update scores list

scal = get_top_scores()

#To get the current scores
@app.route('/current', methods=['POST'])
def current_score():
    scal=get_top_scores() #Refresh scores
    return render_template('index.html', scores=scal)

@app.route('/')
def home():
    global scal
    scal = get_top_scores()  #Refresh scores
    return render_template('index.html', scores=scal)

if __name__ == '__main__':
    #connect to the client and subscribe to "ButtonClick" topic
    client = paho.Client()
    client.on_connect = on_connect
    client.on_message = received_msg
    client.username_pw_set(username="mqttuser",password="temporarypassword")
    client.connect(broker)
    client.subscribe("ButtonClick")
    client.loop_start()

    app.run(debug=True, host='0.0.0.0', port=8000)