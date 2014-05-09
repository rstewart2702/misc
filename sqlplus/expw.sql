column id format 999 heading 'id'
column parent_id format 999 heading 'par|id'
column object_name format a28
column operation format a55
column options format a10 word
column other format a85
column object_node format a20
column other_tag format a30 justify left heading 'OTHER_TAG'
column position format 99999 justify right heading 'posi-|tion'

SELECT id, parent_id, LPAD(' ',2*(LEVEL-1))||operation operation, 
-- rpad(nvl(options,'_'), 10, '_') options,
options,
rpad(nvl(object_name,'_'), 28, '_') object_name,
position
-- , other_tag
, object_node
FROM plan_table
START WITH id = 0 AND statement_id = '&p_name'
CONNECT BY PRIOR id = parent_id AND
statement_id = '&p_name'
order by id
/

select id, object_node, other
from plan_table
where statement_id = '&p_name'
and other is not null
order by id
/