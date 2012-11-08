
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
MondemandStatTypeString = ["unknown", "gauge", "counter"]


#Constants for LWES messages
LWES_LOG_MSG    = "MonDemand::LogMsg"
LWES_STATS_MSG  = "MonDemand::StatsMsg"
LWES_TRACE_MSG  = "MonDemand::TraceMsg"
