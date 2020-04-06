import time, string, random


def generate_order_number():
    generate_time = str(time.strftime('%Y%m%d%H%M%S',
                                      time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
    return random.choice(string.ascii_uppercase) + generate_time
