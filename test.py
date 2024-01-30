import paho.mqtt.client as mqtt
import streamlit as st
import os
from time import sleep


# MQTT settings
MQTT_BROKER = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = "sensor_01_02_time_difference"
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PW = os.getenv("MQTT_PW")


# Streamlit app
st.title("MQTT Metric Display")

# Initialize the metric value
metric_value = 0
st.session_state.time_diff = 0


container = st.container()

# Display the metric
st.metric("Metric Value", metric_value)
st.metric("Metric Value", st.session_state.time_diff)


# Callback function when a message is received
def on_message(client, userdata, message):
    global metric_value
    metric_value = int(message.payload.decode())
    st.session_state.time_diff = metric_value
    print(f"Received value: {metric_value}")
    st.rerun()


# Create an MQTT client
client = mqtt.Client()
client.on_message = on_message


# Connect to the MQTT broker and subscribe to the topic
def connect_to_mqtt():
    client.username_pw_set(username=MQTT_USER, password=MQTT_PW)

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()


# Function to check if MQTT is connected
def is_mqtt_connected():
    return client.is_connected()


# Check MQTT connection and reconnect if necessary
if not is_mqtt_connected():
    print("Connecting to MQTT...")
    connect_to_mqtt()
    print("Connected to MQTT!")

# Display the metric
st.metric("Metric Value", metric_value)
st.metric("Metric Value", st.session_state.time_diff)

container.metric("Metric Value", metric_value)
container.metric("Metric Value", st.session_state.time_diff)
