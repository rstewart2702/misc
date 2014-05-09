set echo off
set verify off

column table_name format a40 wrapped
column index_name format a40 wrapped
column column_name format a40 wrapped
break on table_name

prompt =================================================================================================================
prompt HERE ARE THE INDEXED COLUMNS:

select table_name, index_name, column_name
from all_ind_columns
where table_name like upper('&2.%')
  and index_owner = upper('&1')
order by table_name, index_name, column_position
;




