column owner format a8 wrapped
column constraint_name format a30 wrapped
column constraint_type format a4 heading 'cons|type'
column table_name format a30 wrapped
column r_owner format a8 wrapped
column r_constraint_name format a30 wrapped

prompt Every table that has a foreign key dependency on &1..&2:
select
  owner
, constraint_name
, constraint_type
, table_name
, r_owner
, r_constraint_name
from
  all_constraints
where
    owner = upper('&1')
and constraint_type = 'R'
and r_constraint_name = (select constraint_name from all_constraints where owner = upper('&1')
                         and table_name = upper('&2') and constraint_type = 'P')
;
