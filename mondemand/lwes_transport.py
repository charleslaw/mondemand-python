
from socket import gethostname


from lwes.emitter import LwesEmitter
from lwes.event import LwesEvent
from mondemand.constants import LWES_LOG_MSG, LWES_STATS_MSG, LWES_TRACE_MSG, \
    MondemandStatTypeString


def get_hostname(str_len):
    hostname = gethostname()
    if len(hostname) > str_len:
        hostname = hostname[:1024]

    return hostname


class LwesTransport(object):
    def __init__(self, address, port, interface,
                 heartbeat_flag, heartbeat_frequency, ttl=1):

        #Used to compare LwesTransport instances
        self.config = {'address': address,
                       'interface': interface,
                       'port': port}

        emitter = LwesEmitter(address, interface, port,
                              heartbeat_flag, heartbeat_frequency, ttl=ttl)

        if emitter is None:
            raise Exception('Out of memory')

        self.transport \
            = {
               'log_sender_function': None, #mondemand_transport_lwes_log_sender,
               'stats_sender_function': self.stats_sender,
               'trace_sender_function': self.trace_sender,
               'destroy_function': lambda *args: None, #not needed in Python
               'userdata': emitter
               }


    def trace_sender(self, program_id, owner, trace_id, message, trace_dict):

        hostname = get_hostname(1024)

        event = LwesEvent (None, LWES_TRACE_MSG)
        event.set_STRING("mondemand.prog_id", program_id)
        event.set_STRING("mondemand.trace_id", trace_id)
        event.set_STRING("mondemand.owner", owner)
        event.set_STRING("mondemand.src_host", hostname)
        event.set_STRING("mondemand.message", message)

        for key in trace_dict:
            event.set_STRING(key, trace_dict[key])

        #lwes.lwes_emitter_emit(self.transport['userdata'], event)
        self.transport['userdata'].emit(event)

        return 0


    def stats_sender(self, program_id, stats, contexts):
        message_count = len(stats)
        if message_count > 0:
            event = LwesEvent (None, LWES_STATS_MSG)
            event.set_STRING("prog_id", program_id)


            i = 0
            event.set_U_INT_16("num", message_count)
            for stat_key, stat_value in stats.iteritems():
                event.set_STRING("k%d" % i, stat_key)
                event.set_STRING("t%d" % i,
                                 MondemandStatTypeString[stat_value['type']])
                event.set_INT_64("v%d" % i, stat_value['value'])
                i += 1

            context_count = len(contexts)

            i = 0
            event.set_U_INT_16("ctxt_num", context_count)
            for context_key, context_value in contexts.iteritems():
                event.set_STRING("ctxt_k%d" % i, context_key)
                event.set_STRING("ctxt_v%d" % i, context_value)
                i += 1

            self.transport['userdata'].emit(event)

        return 0


    def __eq__(self, other_object):
        """
        Allows Mondemand clients to make sure the transports are not added twice
        """
        if type(self) != type(other_object):
            return False

        #check the important parameters
        #print "TESTing", self.config, other_object.config
        return self.config == other_object.config
