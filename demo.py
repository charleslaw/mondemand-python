from mondemand.client import MondemandClient
from mondemand.lwes_transport import LwesTransport


m_client = MondemandClient('my_id')


def send_msg(msg):
    sender = LwesTransport('127.0.0.1', 20402, '', 0, 0)

    m_client.add_transport(sender)

    m_client.initialize_trace('joana', 'jo5', msg)

    m_client.set_trace('kkkk1', 'vvvv1')
    m_client.set_trace('kkkk2', 'vvvv2')
    m_client.set_trace('kkkk3', 'vvvv3')

    m_client.flush_trace()
    m_client.clear_trace()


for i in xrange(5):
    send_msg('custom_message')



