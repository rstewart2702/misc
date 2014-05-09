REM      Oracle9i SQL Tuning Workshop

REM      script LI.SQL (list indexes)

REM      usage: @li [table_name]

REM      wildcards in table_name allowed,

REM      and a '%' is appended by default

REM      =====================================



set      termout  off


set      verify   off autotrace off
set      feedback off termout on
break    on table_name skip 1 on index_type
prompt
prompt   indexes on table &&1.%:


select   ui.table_name
,        decode(ui.index_type
               ,'NORMAL', ui.uniqueness
               ,ui.index_type) as index_type
,        ui.index_name
from     user_indexes  ui
where    ui.table_name like upper('&1.%')
order by ui.table_name
,        ui.uniqueness desc
/

@saved_settings
set termout on


