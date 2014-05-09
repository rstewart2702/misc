set verify off
column text format a100 wrapped

select
   dbms_metadata.get_ddl(upper('&1'),upper('&3'),upper('&2')) text
from dual
;
