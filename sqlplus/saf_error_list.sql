rem Dumps out final &&1 rows of saf_error, in order from youngest to oldest.
set verify off

column program format a35 wrapped
column batch format a10 wrapped
column job format a35 wrapped
column object format a35 wrapped
column errmsg format a35 wrapped
column errorstring format a35 wrapped
column errorstack format a35 wrapped

select * from (
  select * from saf_error order by timestamp desc
) where rownum <= &&1
;

set verify on
