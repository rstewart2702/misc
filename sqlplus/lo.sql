column message format a40 word_wrap

select sid, serial#, (sofar/totalwork)*100 pct_done
, message, start_time, last_update_time
from v$session_longops
order by sid, serial#, start_time, last_update_time
/
