
from socket import gethostname


from lwes.emitter import LwesEmitter
from lwes.event import LwesEvent


#Constants for LWES messages
LWES_LOG_MSG    = "MonDemand::LogMsg"
LWES_STATS_MSG  = "MonDemand::StatsMsg"
LWES_TRACE_MSG  = "MonDemand::TraceMsg"


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
               'stats_sender_function': None, #mondemand_transport_lwes_stats_sender,
               'trace_sender_function': self.trace_sender, #mondemand_transport_lwes_trace_sender,
               'destroy_function': None, #mondemand_transport_lwes_destroy,
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


    def __eq__(self, other_object):
        """
        Allows Mondemand clients to make sure the transports are not added twice
        """
        if type(self) != type(other_object):
            return False

        #check the important parameters
        #print "TESTing", self.config, other_object.config
        return self.config == other_object.config
