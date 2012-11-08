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


    m_client.set_context('te1', 'tev1')
    m_client.set_context('te2', 'tev2')
    m_client.set_context('te3', 'tev3')

    m_client.stats_set('stat_ga', 1234)
    m_client.stats_inc('stat_in', value=3)

    m_client.flush_stats()

for i in xrange(5):
    send_msg('custom_message %s' % i)



