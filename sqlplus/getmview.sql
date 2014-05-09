set heading off
set verify off
set long 32786
column q format a120 wrapped

select
  dbms_metadata.get_ddl('MATERIALIZED_VIEW',upper('&2'),upper('&1')) q
from dual;

set verify on
set heading on
