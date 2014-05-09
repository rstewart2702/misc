compute sum of tot_use on report
break on report
set verify off

select
  vt.segtype,
--  vt.session_num,
  vs.sid
, to_char(sysdate, 'hh24:mi:ss dd-mon-yyyy') time_stamp
, sum(vt.blocks * v.blocksize)/1024/1024 tot_use
from
  v$sort_usage vt
, (select to_number(value) blocksize from v$parameter where upper(name) = 'DB_BLOCK_SIZE') v
, v$session vs
where
    vt.session_num = vs.serial#
and vs.osuser = '&1'
group by
--  vt.session_num,
vt.segtype
, vs.sid
/
