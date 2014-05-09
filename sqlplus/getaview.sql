rem getaview.sql - extract any view...
rem from _Expert One-on-one Oracle_ by Tom Kyte
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

spool &2..sql
prompt create or replace view &1..&2 (
select decode(column_id,1,'',',') || column_name column_name
from all_tab_columns
where table_name = upper('&2')
and owner = upper('&1')
order by column_id
/
prompt ) as
select text
from all_views
where view_name = upper('&2')
and owner = upper('&1')
/
prompt /
spool off

set termout on
set heading on
set feedback on
set verify on
set timing on
