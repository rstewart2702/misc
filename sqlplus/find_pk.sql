column constraint_name format a25
column column_name format a35
set verify off

prompt Primary key constraint for &&1..&&2:
select constraint_name, column_name, position
from dba_cons_columns
where owner = upper('&&1')
  and table_name = upper('&&2')
and constraint_name = (
      select constraint_name
      from dba_constraints
      where owner = upper('&&1')
        and constraint_type = 'P'
        and table_name = upper('&&2')
    )
order by
  constraint_name
, position
;
