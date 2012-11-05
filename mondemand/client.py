#TODO: Add mondemand_logs

from lwes_transport import LwesTransport


#Constants
M_LOG_EMERG     =  0   # system is unusable
M_LOG_ALERT     =  1   # action must be taken immediately
M_LOG_CRIT      =  2   # critical conditions
M_LOG_ERR       =  3   # error conditions
M_LOG_WARNING   =  4   # warning conditions
M_LOG_NOTICE    =  5   # normal but significant condition
M_LOG_INFO      =  6   # informational
M_LOG_DEBUG     =  7   # debug-level messages
M_LOG_ALL       =  8   # all messages, including traces
M_LOG_WARN  = M_LOG_WARNING
M_LOG_ERROR = M_LOG_ERR

MONDEMAND_INC = 0
MONDEMAND_DEC = 1
MONDEMAND_SET = 3

MONDEMAND_UNKNOWN = 0
MONDEMAND_GAUGE   = 1
MONDEMAND_COUNTER = 2



class MondemandClient(object):
    def __init__(self, program_id):
        if program_id is None:
            raise Exception

        self.program_id =  program_id

        #transports
        self.transports = []

        #Trace information - resets traces & trace owner information
        self.clear_trace()
        #Start with no stats
        self.stats = {}
        #Reset contexts
        self.remove_all_contexts()

        self.logs = {'messages': {},
                     'immediate_send_level': M_LOG_CRIT,
                     'no_send_level': M_LOG_NOTICE,
                     }

    def add_transport(self, transport):
        if transport is None:
            raise Exception('Invalid transport')

        if transport not in self.transports:
            self.transports.append(transport)

        return

    def flush():
        #TODO: Add flush_logs
        self.flush_stats()
        self.flush_trace()


    """
    Trace Functions
    """
    def clear_trace(self):
        self.remove_all_traces()
        self.trace_info = {}

    def initialize_trace(self, owner, trace_id, message):
        self.trace_info = {
                           'trace_id': trace_id,
                           'owner': owner,
                           'trace_message': message
                           }

    def remove_all_traces(self):
        #Resets the traces
        self.trace = {}

    def set_trace(self, key, value):
        """
        sets a trace item, overwriting it if it is already set
        """
        if key is None or value is None:
            raise Exception('Invalid trace key/value')

        #TODO: If needed, replace this dict with m_hash_table
        self.trace[key] = value

    def remove_trace(self, key):
        if key in self.trace:
            self.trace.pop(key)

    def flush_trace(self):
        if self.trace_info:
            #Looks like we can dispatch something
            #TODO: What happens when a trace is initialized w/o anything??
            #     Still send the message?
            for transport in self.transports:
                #send the trace
                trace_sender = transport.transport.get('trace_sender_function')
                if trace_sender:
                    status = trace_sender(self.program_id,
                                          self.trace_info['owner'],
                                          self.trace_info['trace_id'],
                                          self.trace_info['trace_message'],
                                          self.trace)

    def get_trace(self, key):
        return self.trace.get(key)

    def get_trace_keys():
        return self.trace.keys()



    """
    Stats Functions
    """
    def reset_stats(self):
        keys = self.stats.keys()
        for key in keys:
            self.stat[key]['value'] = 0

    def stats_perform_op(self, op, type, key, value):
        """
        Only support key (do not support filename & line as keys)
        """
        if key not in self.stats:
            #always start with a zeroed stat
            self.stats[key] = {'type': type,
                               'value': 0}
        else:
            #TODO: should I really reset the type?
            self.stats[key]['type'] = type

        mond_op = {MONDEMAND_INC: lambda value, dv: value + dv,
                   MONDEMAND_DEC: lambda value, dv: value - dv,
                   MONDEMAND_SET: lambda old, value: value,
                   }

        # depending on operation change value
        if op in mond_op:
            self.stats[key]['value'] = mond_op[op](self.stats[key]['value'],
                                                   value)

    def stats_inc(self, key, value=1):
        """
        Incriment a given stat by a specified value.  If not value is specified
        the stat is incrimented by 1.  This is a COUNTER.
        """
        self.stats_perform_op(MONDEMAND_INC, MONDEMAND_COUNTER, key, value)

    def stats_dec(self, key, value=1):
        """
        Decrement a given stat by a specified value.  If not value is specified
        the stat is decremented by 1.  This is a COUNTER.
        """
        self.stats_perform_op(MONDEMAND_DEC, MONDEMAND_COUNTER, key, value)

    def stats_set(self, key, value):
        """
        Set a gague stat to a specified value.This is a GAUGE.
        """
        self.stats_perform_op(MONDEMAND_SET, MONDEMAND_GAUGE, key, value)



    """
    Context Functions
    TODO: These are used for stats, but are they used for logs as well
    """
    def get_context(self, key):
        """
        Return the context with the given key
        If the context does not exist, return None
        """
        return self.contexts.get(key)

    def get_context_keys(self):
        """
        Return the list of context keys
        """
        return self.contexts.keys()

    def set_context(self, key, value):
        """
        Set the given context.  Update the context if it already exists.
        """
        self.contexts[key] = value

    def remove_context(self, key):
        """
        Remove the given context if it exists
        """
        if key in self.contexts:
            self.contexts.pop(key)

    def remove_all_contexts(self):
        self.contexts = {}

