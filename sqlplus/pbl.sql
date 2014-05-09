set verify off

select line, text
from user_source
where type in ('PACKAGE BODY', 'PROCEDURE', 'FUNCTION') and name = upper('&1')
and &2 <= line and line <= &3
order by line;

set verify on

