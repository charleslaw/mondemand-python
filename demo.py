from mondemand.client import MondemandClient
from mondemand.lwes_transport import LwesTransport


#Create a client
m_client = MondemandClient('my_program')

sender = LwesTransport('127.0.0.1', 20402, '', 0, 0)
m_client.add_transport(sender)


def send_msg(msg):
    m_client.initialize_trace('fluke', 'fp', msg)

    m_client.set_trace('key1', 'val1')
    m_client.set_trace('key2', 'val2')
    m_client.set_trace('key3', 'val3')

    m_client.flush_trace()
    m_client.clear_trace()


for i in xrange(5):
    send_msg('custom_message %s' % i)



