from worker import worker
import requests

from src.helpers.general_helper import get_app_config

from src.helpers.redis_helper import RedisHelper

from src.helpers.general_helper import make_hash_from_dictionary

from src.helpers.general_helper import logging_messages, chunks

from src.repositories.last_transactions_repository import LastTransactionsRepository

from datetime import datetime, date

from src.repositories.statistics_repository import StatisticsRepository

import time

app_config = get_app_config()

redis_helper = RedisHelper(**app_config['redis']['data_storage']['con'])

last_transactions_repository = LastTransactionsRepository()
statistics_repository = StatisticsRepository()


@worker.task(bind=True, queue="beat_move_data_to_db")
def beat_move_data_to_db(self, ):
    try:

        try:

            api_response = requests.get(app_config['bitexen']['api_url'])

        except Exception as ex:

            message = "Bitexen apiye bağlanılamıyor "
            logging_messages(message, type="error", exc_info=False)

            return False

        if int(api_response.status_code) == 200:

            resp_body = api_response.json()

            if "last_transactions" in resp_body['data']:

                converted_transactions = []
                for transaction in resp_body['data']["last_transactions"]:

                    transaction_hash = make_hash_from_dictionary(transaction)

                    transaction_is_exist = redis_helper.get(transaction_hash)

                    if transaction_is_exist is not None:
                        message = "bu transaction zaten daha önce eklenmiş " + str(transaction)
                        logging_messages(message, type="warning", exc_info=False)

                        continue
                    else:

                        try:

                            redis_helper.set_with_expire(key=transaction_hash,
                                                         value="",
                                                         expire_time_sec=app_config['redis']['data_storage'][
                                                             'general_object_cache_time_seconds'],
                                                         expire_callback=float)

                        except Exception as ex:

                            message = "Redise yazarken bir sorun oluştu"
                            logging_messages(message, type="error", exc_info=False)
                            continue

                        transaction['time'] = datetime.fromtimestamp(float(transaction['time']))
                        transaction['amount'] = float(transaction['amount'])
                        transaction['price'] = float(transaction['price'])
                        transaction['transaction_hash'] = transaction_hash

                        converted_transactions.append(transaction)

                        message = "Bu transaction db ye eklendi " + str(transaction)
                        logging_messages(message, type="info", exc_info=False)

                if len(converted_transactions) > 0:

                    data_list_packets = list(chunks(converted_transactions, 50))

                    for data_list_packet in data_list_packets:

                        try:

                            last_transactions_repository.add_range(data_list_packet)

                        except Exception as ex:

                            # Eğer bu bulk list eklenemedi ise, bu kayıtları redisten de siliyoruz
                            for i in data_list_packet:
                                redis_helper.remove(i['transaction_hash'])

                            message = "Mongodbye yazarken bir sorun oluştu"
                            logging_messages(message, type="error", exc_info=False)
                            continue






    except Exception as ex:
        self.retry(countdown=10, exc=ex, max_retries=3)

    return True


@worker.task(bind=True, queue="beat_calculate_statistics")
def beat_calculate_statistics(self):
    stat_periods = ["daily", "weekly", "monthly"]
    stat_types = ["min_price", "max_price", "average_price", "total_volume"]

    todays_date = date.today()

    year = todays_date.year
    month = todays_date.month
    week = todays_date.isocalendar()[1]
    day = todays_date.day

    start = datetime(year=year, month=month, day=day, hour=00, minute=00, second=00)
    end = datetime(year=year, month=month, day=day, hour=23, minute=59, second=59)

    transactions = last_transactions_repository.get_all(
        predicate={
            'time': {
                '$lte': end,
                '$gte': start
            }
        },
        fields={'_id', 'amount', 'price', 'type'},
        skip=0,
        limit=420
    )

    prices = []

    transactions_list = list(transactions)
    transactions_id_list = []

    if len(transactions_list) == 0:
        return False

    for i in transactions_list:
        prices.append(i['price'])
        transactions_id_list.append(i['_id'])

    for stat_period in stat_periods:

        if stat_period == "daily":
            date_key = str(year) + "|" + str(month) + "|" + str(week) + "|" + str(day)
        elif stat_period == "weekly":
            date_key = str(year) + "|" + str(month) + "|" + str(week)
        elif stat_period == "monthly":
            date_key = str(year) + "|" + str(month)

        for stat_type in stat_types:

            predicate = {
                "stat_period": stat_period,
                "date_key": date_key,
                "stat_type": stat_type
            }

            value = {}

            stat_row = statistics_repository.get_single(predicate=predicate)

            if stat_row is None:
                stat_row = {
                    "stat_period": stat_period,
                    "date_key": date_key,
                    "last_calculated_date": datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                              '%Y-%m-%d %H:%M:%S.%f'),
                    "stat_type": stat_type,
                    "quantity": 0,
                    "total_amount_count": 0,
                    "year": year,
                    "month": month,
                    "week": week,
                    "day": day,
                }

                try:

                    statistics_repository.add(stat_row)

                except Exception as ex:

                    message = "İstatistik satırı db ye eklenirken bir hata oluştu"
                    logging_messages(message, type="error", exc_info=False)
                    return False

            if stat_row['stat_type'] == "min_price":

                if stat_row['quantity'] == 0:

                    value['quantity'] = min(prices)
                elif stat_row['quantity'] > 0:
                    prices.append(stat_row['quantity'])

                    value['quantity'] = min(prices)
            elif stat_row['stat_type'] == "max_price":

                if stat_row['quantity'] == 0:

                    value['quantity'] = max(prices)
                elif stat_row['quantity'] > 0:
                    prices.append(stat_row['quantity'])

                    value['quantity'] = max(prices)

            elif stat_row['stat_type'] == "average_price":

                total_quantity = stat_row['total_amount_count'] * stat_row['quantity']
                sum_total_amount_count = stat_row['total_amount_count']

                for i in transactions_list:

                    if i['type'] == "S":
                        continue

                    total_quantity = total_quantity + (i['price'] * i['amount'])

                    sum_total_amount_count = sum_total_amount_count + i['amount']

                value['quantity'] = float(total_quantity / sum_total_amount_count)
                value['total_amount_count'] = sum_total_amount_count

            elif stat_row['stat_type'] == "total_volume":
                total_quantity = stat_row['quantity']

                for i in transactions_list:
                    total_quantity = total_quantity + (i['price'] * i['amount'])

                value['quantity'] = total_quantity

            value["last_calculated_date"] = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                              '%Y-%m-%d %H:%M:%S.%f')

            statistics_repository.edit(predicate=predicate, value=value)

            # Transaction satırlarını artık silebiliriz
            predicate = {
                "_id": {"$in": transactions_id_list}
            }
            last_transactions_repository.remove_range(predicate)


@worker.task(bind=True, queue="beat_aykut_worker")
def beat_aykut_worker(self, ):
    time.sleep(15)

    response = {
        "result": "selçuk"
    }

    return response


@worker.task(bind=True, queue="worker_topla")
def worker_topla(self, a, b):
    print(str(a) + "+" + str(b) + " toplama işlemi başladı...")

    time.sleep(60)

    print(str(a) + "+" + str(b) + " toplama işlemi bitti...")

    return a + b
