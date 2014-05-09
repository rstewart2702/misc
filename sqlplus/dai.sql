REM    Oracle9i:  SQL Tuning Workshop

REM    script DAI.SQL (drop all indexes)

REM    prompts for a table name; % is appended

REM    =======================================

accept TABLE_NAME  prompt "     on which table: "

set    termout off

store  set saved_settings replace

set    heading off verify off autotrace off feedback off

spool  doit.sql


select 'DROP INDEX '||ui.index_name||';'
from   user_indexes ui
where  table_name like upper('&TABLE_NAME.%')
/

spool  off

set    termout on

@doit

@saved_settings

undef  TABLE_NAME

set    termout on

