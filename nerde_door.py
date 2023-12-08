import paho.mqtt.client as mqtt


def opendoor():

    def on_connect(client, userdata, flags, rc):
        client.subscribe("NeRDDOOR/nerd/RFID")

    def publish(topic, message, waitForAck = False):
        client.publish(topic, message, 2)


    client = mqtt.Client()
    client.username_pw_set("NeRDDOOR","nerdU@2020")
    client.on_connect = on_connect
    client.connect("192.168.2.20",1883,60)
    client.loop_start()


    publish("NeRDDOOR/nerd/State","Open")
    client.loop_stop()
    client.disconnect()
    return
    

