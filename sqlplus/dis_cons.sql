set heading off
set long 999999999
set feedback off
set linesize 1000
set trimspool on
set verify off
rem set termout off
set embedded on
set timing off

select 'alter table '||table_name||' disable constraint '||constraint_name||';'
from all_constraints
where table_name = upper('&2') and owner = upper('&1')
;


set termout on
set heading on
set feedback on
set verify on
set timing on
