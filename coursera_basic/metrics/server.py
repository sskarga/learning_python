"""
Сервер для приема метрик
"""

import asyncio

class ClientError(Exception):
    """ исключение ClientError """
    pass


class ClientSocketError(ClientError):
    """ исключение ClientSocketError """
    pass


class ClientProtocolError(ClientError):
    """ исключение ClientProtocolError """
    pass


class ClientServerProtocol(asyncio.Protocol):

    operations = ['get', 'put']
    request_parameters = []
    metrics = {}

    def process_get(self):
        # ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n
        if self.request_parameters[0] in "*":
            # get all
            result = "ok\n"
            for key in self.metrics:
                for i in range(0, len(self.metrics[key])):
                    result += "{0} {1} {2}\n".format(key, self.metrics[key][i][1], self.metrics[key][i][0])

        else:
            if self.metrics.get(self.request_parameters[0]) is None:
                result = "error\nNon existing key\n"
            else:
                result = "ok\n"
                key = self.request_parameters[0]
                for i in range(0, len(self.metrics[key])):
                    result += "{0} {1} {2}\n".format(key, self.metrics[key][i][1], self.metrics[key][i][0])

        return result

    def process_put(self):
        # client.put("palm.cpu", 0.5, timestamp=1150864247)
        if len(self.request_parameters) == 3:
            ls_metric = (int(self.request_parameters[2]), float(self.request_parameters[1]))

            if self.metrics.get(self.request_parameters[0]) is None:
                self.metrics[self.request_parameters[0]] = [ls_metric]
            else:
                self.metrics[self.request_parameters[0]].append(ls_metric)
            result = "ok\n"
        else:
            result = "error\nwrong number of parameters in command\n"

        return result

    def dispatch(self, value):
        method_name = 'process_' + str(value)
        method = getattr(self, method_name)
        return method()

    def process_data(self, cmd_string):
        request = cmd_string.lower().split()

        result = "error\nwrong command\n"

        if self.operations.count(request[0]) > 0:
            self.request_parameters.clear()
            self.request_parameters = request[1:]
            result = self.dispatch(request[0])

        return result + "\n"

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())


loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8181
)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()