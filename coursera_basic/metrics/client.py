"""
Клиент для отправки метрик

Команды
--------------------------------------------------
put - для сохранения метрик на сервере.
put <key> <value> <timestamp>\n

value - вещественное число

Успешный ответ от сервера: ok\n\n
Ошибка сервера: error\nwrong command\n\n

get - для получения метрик.
get <key>\n

Успешный ответ от сервера: ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n
Если ни одна метрика не удовлетворяет условиям поиска, то вернется ответ: ok\n\n

Реализация клиента.
====================================================
    client = Client("127.0.0.1", 8888, timeout=15) - timeout (timeout=None по умолчанию)

    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)

    print(client.get("*"))

Клиент получает данные в текстовом виде, метод get должен возвращать словарь с полученными ключами с сервера.
Значением ключа в словаре является список кортежей [(timestamp, metric_value), ...], отсортированный по timestamp
от меньшего к большему. Значение timestamp должно быть преобразовано к целому числу int. Значение метрики metric_value
нужно преобразовать к числу с плавающей точкой float.

Метод put принимает первым аргументом название метрики, вторым численное значение, третьим -
необязательный именованный аргумент timestamp. Если пользователь вызвал метод put без аргумента timestamp,
то клиент автоматически должен подставить текущее время в команду put - str(int(time.time()))

Метод put не возвращает ничего в случае успешной отправки и выбрасывает исключение ClientError в случае неуспешной.
Метод get возвращает словарь с метриками (смотрите ниже пример) в случае успешного получения ответа от сервера
и выбрасывает исключение ClientError в случае неуспешного.

client.get("palm.cpu"):
    {
      'palm.cpu': [
        (1150864247, 0.5),
        (1150864248, 0.5)
      ]
    }

client.get("*"):
    {
      'palm.cpu': [
        (1150864247, 0.5),
        (1150864248, 0.5)
      ],
      'eardrum.cpu': [
        (1150864250, 3.0),
        (1150864251, 4.0)
      ],
      'eardrum.memory': [
        (1503320872, 4200000.0)
      ]
    }

client.get("non_existing_key")
    {} - пустой словарь
"""

import socket
import time
import operator


class ClientError(Exception):
    """ исключение ClientError """
    pass


class ClientSocketError(ClientError):
    """ исключение ClientSocketError """
    pass


class ClientProtocolError(ClientError):
    """ исключение ClientProtocolError """
    pass


class Client(object):
    """ Клиент для отправки метрик """

    def __init__(self, ip, port, timeout=None):
        """Constructor"""
        self.ip = ip
        self.port = port
        self.timeout = timeout

    def _send(self, command):

        result = []

        with socket.create_connection((self.ip, self.port), self.timeout) as sock:
            sock.settimeout(self.timeout)

            try:
                sock.sendall(command.encode("utf8"))

                rdata = ""

                while rdata[-2:] != "\n\n":
                    data = sock.recv(1024)
                    rdata += data.decode("utf8")

                msg = rdata.splitlines()

                if not (msg[0].lower() in "ok"):
                    raise ClientProtocolError("{0} - {1}".format(msg[0], msg[1]))

                if len(msg) > 2:
                    result = msg[1:-1]

            except socket.timeout:
                raise ClientSocketError("send data timeout")

            except socket.error as ex:
                raise ClientSocketError("send data error:", ex)

        return result

    def get(self, key):
        """Получения метрик"""
        metrics = {}

        msg = self._send("get {0}\n".format(key))

        for i in range(0, len(msg)):
            metric = msg[i].split()
            ls_metric = (int(metric[2]), float(metric[1]))

            if metrics.get(metric[0]) is None:
                metrics[metric[0]] = [ls_metric]
            else:
                metrics[metric[0]].append(ls_metric)

        for key in metrics:
            sorted(metrics[key], key=operator.itemgetter(0))  # key=lambda x: x[1]

        return metrics

    def put(self, key, value, timestamp=None):
        """
            Cохранения метрик на сервере
        """
        if timestamp is None:
            timestamp = str(int(time.time()))

        self._send("put {0} {1} {2}\n".format(key, value, timestamp))
