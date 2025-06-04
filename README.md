# IoT Reaction Speed Tracker with Secure Cloud Integration

This project is a complete IoT-based reaction time tracker built using Raspberry Pi and a secure cloud infrastructure. It integrates Python, a Linux Kernel Module (LKM), MQTT protocol, Flask web application, and AWS services (EC2 and DynamoDB) to measure, transmit, store, and visualize user reaction times.

## 🚀 Features

- Measures human reaction speed using a button, buzzer, and LED on a Raspberry Pi.
- Uses Python and LKM to control GPIO components.
- Transmits data securely via MQTT with authentication.
- Web application hosted on AWS EC2 using Flask.
- Stores player data in AWS DynamoDB.
- Displays the top 10 fastest players on a web leaderboard.
- Secure MQTT and EC2 configurations for protection against unauthorized access.

## 🛠️ Technologies Used

- **Hardware**: Raspberry Pi, LED, Buzzer, Push Button, Breadboard
- **Programming**: Python, Linux Kernel Module (C), Flask (Python)
- **IoT Messaging**: MQTT (Mosquitto)
- **Cloud Infrastructure**:
  - AWS EC2 (Flask Web App & MQTT Broker)
  - AWS DynamoDB (NoSQL Database)

## 📦 Installation and Setup

### 1. Raspberry Pi Setup
- Connect:
  - **LED**: GPIO23 and GND via resistor
  - **Button**: GPIO16 and 3.3V via resistor
  - **Buzzer**: GPIO25 and GND
- Install dependencies:
  ```bash
  sudo apt update
  sudo apt install mosquitto mosquitto-clients
  pip install paho-mqtt

## 🎥 Demo Video

Watch the full demo here: 

[![Watch on YouTube](https://img.youtube.com/vi/DpEk_6M3_Rg/0.jpg)](https://www.youtube.com/watch?v=DpEk_6M3_Rg)
