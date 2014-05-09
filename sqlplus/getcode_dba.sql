rem getcodel.sql - extract any procedure, function or package
rem from _Expert One-on-one Oracle_ by Tom Kyte
rem this version simply lists the code to the terminal, instead of putting it into a text file...
set feedback off
set heading off
set termout off
set linesize 1000
set trimspool on
set verify off
set timing off
spool &2..sql
prompt set define off
select decode( type||'-'||to_char(line,'fm99999'), 
                'PACKAGE BODY-1', '/'||chr(10),
                null) ||
       decode(line,1,'create or replace ', '' ) ||
       text text
from dba_source
where name = upper('&&2')
and owner = upper('&&1')
order by type, line;
prompt /
prompt set define on
spool off
set feedback on
set heading on
set termout on
set linesize 100
set timing on