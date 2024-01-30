import pandas as pd
import datetime
import paho.mqtt.client as mqtt

# MQTT settings
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic_peso = "ufg_alexandreacff_peso"
mqtt_topic_velz = "ufg_alexandreacff_velz"
mqtt_topic_dist = "ufg_alexandreacff_dist"

# Create an empty DataFrame
df = pd.DataFrame(columns=['timestamp', 'peso', 'velz', 'dist'])

def line_is_complete(new_row):
    if new_row['peso'] is not None and new_row['velz'] is not None and new_row['dist'] is not None:
        return True
    else:
        return False

new_row = {'timestamp': None, 'peso': None, 'velz': None, 'dist': None}

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    global new_row
    global df

    sensor_data = msg.payload.decode("utf-8")
    print(f"Received sensor data: {sensor_data}")

    # Get the current timestamp
    timestamp = datetime.datetime.now()
    
    new_row['timestamp'] = timestamp

    # Update the appropriate field of new_row based on the topic of the message
    if msg.topic == mqtt_topic_peso:
        new_row['peso'] = sensor_data
    elif msg.topic == mqtt_topic_velz:
        new_row['velz'] = sensor_data
    elif msg.topic == mqtt_topic_dist:
        new_row['dist'] = sensor_data

    complete_line = line_is_complete(new_row)

    if complete_line:
        # Append row to the DataFrame
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df])
        df.to_csv('data/data_0.csv')
        # Reset new_row
        new_row = {'timestamp': timestamp, 'peso': None, 'velz': None, 'dist': None}


# Set up the MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the MQTT topic
client.subscribe(mqtt_topic_peso)
client.subscribe(mqtt_topic_dist)
client.subscribe(mqtt_topic_velz)

# Loop to listen for messages
client.loop_forever()