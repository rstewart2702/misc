select s.username, p.spid, s.sid, s.serial#
from v$session s, v$process p
where s.paddr = p.addr
/
