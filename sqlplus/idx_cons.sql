set echo off
set verify off

rem 12-19-2003
rem This is very handy when you are trying to compare the index and constraint settings
rem for a pair of similarly-named tables (works to display indexed columns and constraints
rem for a single table as well...). So, it is particularly handy when looking into issues
rem with the partitioned tables and their single-month-of-data counterparts.
rem

column table_name format a40 wrapped
column index_name format a60 wrapped
column column_name format a40 wrapped
column search_condition format a30 wrapped
column constraint_info format a40 wrapped
break on table_name

prompt =================================================================================================================
prompt HERE ARE THE INDEXED COLUMNS:

select c.table_name, c.index_name||' ('||i.index_type||', '||i.uniqueness||')' index_name, c.column_name
from all_ind_columns c, all_indexes i
where c.table_name like upper('&2.%')
  and c.index_owner = upper('&1')
  and i.owner = upper('&1')
  and i.index_name = c.index_name
order by table_name, index_name, column_position
;

prompt =================================================================================================================
prompt HERE IS THE CONSTRAINT INFORMATION:

select constraint_name, constraint_type, table_name
, search_condition
, r_owner||decode(r_owner, null, null, '.')||r_constraint_name constraint_info
, status, rely, invalid, deferrable, deferred
, validated, generated
from all_constraints
where table_name like upper('&2.%')
  and owner = upper('&1')
order by table_name, constraint_type, constraint_name
;

