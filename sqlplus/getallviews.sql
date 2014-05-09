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

spool tmp.sql
select '@getaview &1 ' || view_name
from user_views
/
spool off

set termout on
set heading on
set feedback on
set verify on
@tmp
set timing on
