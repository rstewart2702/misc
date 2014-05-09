set heading off
set long 999999999
set feedback off
set linesize 1000
set trimspool on
set verify off
rem set termout off
set embedded on
set timing off

select 'create '||nvl(uniqueness,' ')||
       ' index '||index_name||
       ' on '||table_name
from all_indexes
where index_name = upper('&2') and owner = upper('&1')
;

select 
  decode(rownum, 1, '( '||column_name, ', '||column_name)
from
  all_ind_columns
where
     index_name = upper('&2') and index_owner = upper('&1')
;

prompt )

select 'pctfree '||pct_free||chr(10)||
       ' initrans '||ini_trans||chr(10)||
       ' maxtrans '||max_trans||chr(10)||
       ' tablespace '||tablespace_name||chr(10)||
       ' storage (initial '||initial_extent||chr(10)||
       decode(next_extent, null, '', '          next    '||next_extent||chr(10))||
       '          minextents '||min_extents||chr(10)||
       '          maxextents '||max_extents||chr(10)||
       '          pctincrease 0 buffer_pool default freelists 5'||chr(10)||
       '         ) nologging parallel(degree '||degree||')'
from all_indexes
where index_name = upper('&2') and owner = upper('&1')
;

set termout on
set heading on
set feedback on
set verify on
set timing on
