import paho.mqtt.client as mqtt
import traceback

broker_source = "127.0.0.1"
broker_source_port = 1883
broker_target = "YourBroker"
broker_target_port = 1883

client_source = mqtt.Client("YourClientIdSource")
client_target = mqtt.Client("YourClientIdTarget")

client_source.username_pw_set("YourUsernameSource", "YourPasswordSource")
client_target.username_pw_set("YourUsernameTarget", "YourPasswordTarget")

def on_message(client, userdata, message):
	"Evaluated when a new message is received on a subscribed topic"
	print("Received message '" + str(message.payload)[2:][:-1] + "' on topic '"
		+ message.topic + "' with QoS " + str(message.qos))
	if not filterMessage(str(message.payload)[2:][:-1], str(message.topic), (message.qos)):
		client_target.publish(message.topic, str(message.payload)[2:][:-1], message.qos, retain=False)

def setup():
	"Runs the setup procedure for the client"
	print("Setting up the onMessage handler")
	client_source.on_message = on_message
	print("Connecting to source")
	client_source.connect(broker_source, broker_source_port)
	print("Connecting to target")
	client_target.connect(broker_target, broker_target_port)
	client_source.subscribe("#", qos=1)
	print("Setup finished, waiting for messages...")

def filterMessage(payload, topic, qos):
	"Filters the messages depending on the configuration for the attributes payload, topic and QoS. 'True' means that the message is not forwarded."
	# Examples below:
	if(payload == "10 %"):
		print('Filtered: payload == "10 %"')
		return True
	if(topic == "humidity" and qos == 0):
		print('Filtered: topic == "humidity" and qos == 0')
		return True
	if(topic == "temperature" or qos == 2):
		print('Filtered: topic == "temperature" or qos == 2')
		return True
	#Add your filters here

try:
	setup()
	client_source.loop_forever()
	client_target.loop_forever()
except Exception as e:
	traceback.print_exc()