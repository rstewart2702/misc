select 'host orakill antioch2 '||spid x
from v$process p, v$session s
where p.addr = s.paddr
and osuser like 'AL10015L2N320CJ\IWAM%'
/
