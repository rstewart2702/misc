set heading off
set long 999999999
set feedback off
set linesize 1000
set trimspool on
set verify off
set termout off
set embedded on
set timing off

column column_name format a1000
column text format a1000

spool tmp.sql
select '@getcode &1 '|| name
from (
  select distinct name
  from all_source
  where owner = upper('&1')
)
/
spool off

set termout on
set heading on
set feedback on
set verify on
@tmp
set timing on
