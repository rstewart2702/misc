column trigger_body format a250 wrapped
column description format a250 wrapped
set long 32768
set feedback off
set heading off
rem set termout off
set linesize 1000
set trimspool on
set verify off
set timing off

prompt set define off
-- select 'create trigger '||'&&2' from dual;
prompt create trigger

select description
from all_triggers
where 
    owner = upper('&&1')
and trigger_name = upper('&&2');

select trigger_body
from all_triggers
where owner = upper('&&1')
and trigger_name = upper('&&2');

prompt /
prompt set define on

set feedback on
set heading on
set termout on
set linesize 100
set timing on
