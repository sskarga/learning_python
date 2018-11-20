from client import Client

cl = Client("127.0.0.1", 8181, 15)
cl.put("cpu", 1.3)
client1 = Client("127.0.0.1", 8181, 15)
client2 = Client("127.0.0.1", 8181, 15)
client1.put("k1", 0.25, timestamp=1)
client2.put("k1", 2.156, timestamp=2)
client1.put("k1", 0.35, timestamp=3)
client2.put("k2", 30, timestamp=4)
client1.put("k2", 40, timestamp=5)
client1.put("k2", 40, timestamp=5)