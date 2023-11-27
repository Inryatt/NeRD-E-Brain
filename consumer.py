from kafka import KafkaConsumer

consumer = KafkaConsumer('nerdj_np',bootstrap_servers='localhost:9094',client_id="consumear_test", group_id='nerd-e')
for msg in consumer:
    print (msg)


