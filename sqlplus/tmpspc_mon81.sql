compute sum of tot_use on report
break on report
set verify off

select
  vpx.qcsid
, vt.segtype
--  vt.session_num,
, vs.sid
, to_char(sysdate, 'hh24:mi:ss dd-mon-yyyy') time_stamp
, sum(vt.blocks * v.blocksize)/1024/1024 tot_use
from
  v$sort_usage vt
, (select to_number(value) blocksize from v$parameter where upper(name) = 'DB_BLOCK_SIZE') v
, v$session vs
, v$px_session vpx
where
    vt.session_addr = vs.saddr
and vs.osuser = '&1'
and vs.status = 'ACTIVE'
-- and vs.sid in (select sid from v$px_session where qcsid = )
and vs.sid = vpx.sid(+)
group by
--  vt.session_num,
vt.segtype
, vs.sid
, vpx.qcsid
order by
  vpx.qcsid
, vt.segtype
, vs.sid
/
