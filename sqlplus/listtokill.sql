rem This is designed to mainly be of use on my local Oracle instance...
begin dbms_output.put_line(to_char(sysdate,'mm-dd-yyyy hh24:mi:ss')); end;
/
column program format a14 trunc
set line 250

select spid, sid, osuser, s.program, s.status, s.username, p.username
from v$process p, v$session s where p.addr=s.paddr
;


