prompt
prompt COLUMNS AND COMMENTS FOR &1..&2:

column comments format a80 word
column column_name format a32 word
set verify off

select cc.column_name, cc.comments
from all_col_comments cc, all_tab_columns tcol
where cc.table_name = tcol.table_name and cc.column_Name = tcol.column_name
and cc.owner = upper('&1') and cc.table_name = upper('&2')
and tcol.owner = cc.owner
order by tcol.column_id
;

set verify on
