from kafka import KafkaProducer


def main():
    producer = KafkaProducer(bootstrap_servers='localhost:9094', client_id='prod_bonito',acks="all")
    for _ in range(1):
        producer.send('nerdj_play', b'dance dance til youre dead')

    producer.flush()


if __name__ == '__main__':
    main()