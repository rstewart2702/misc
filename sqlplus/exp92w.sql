column id format 999 heading 'id'
column parent_id format 999 heading 'par|id'
column object_name format a20 wrap
column operation format a125 wrap
column options format a10 word
column other format a85
column object_node format a15
column other_tag format a29 wrap justify left heading 'OTHER_TAG'
column position format 999999999 justify right heading 'posi-|tion'
column optimizer format a12 justify left
column distribution format a20 
column partition_start format a10 wrap justify left heading 'prtn|start'
column partition_stop format a10 wrap justify left heading 'prtn|stop'
column partition_id format 9999 heading 'prtn|id'
column access_predicates format a85 wrap heading 'access|predicates'
column filter_predicates format a85 wrap heading 'filter|predicates'
column temp_space format 999999999
column cpu_cost format 999999999
column io_cost format 999999999
set linesize 1000
set verify off

set long 65536

SELECT 
  id
, parent_id
, LPAD(' ',2*(LEVEL-1))||operation||
   decode(options, null, null, ' (') || options || decode(options, null, null, ')')||
   decode(object_name, null, null, ' of '||object_owner||'.'||object_name)||
   decode(cost||cardinality||bytes, null, null, ' (')||
   decode(cost, null, null, 'cost='||cost||decode(cardinality, null, null, ' '))||
   decode(cardinality, null, null, 'card='||cardinality||decode(bytes, null, null, ' '))||
   decode(bytes, null, null, 'bytes='||bytes)||
   decode(cost||cardinality||bytes, null, null, ')')
   -- ' (cost:'||cost||' card:'||cardinality||')'||
  operation
-- , rpad(nvl(options,' '), 10, ' ') options
-- , options
--, rpad(nvl(object_name,' '), 28, ' ') object_name
-- , object_name
, position
, optimizer
, other_tag
, object_node
, distribution
, partition_id
, partition_start
, partition_stop
-- , access_predicates
-- , filter_predicates
, cpu_cost
, io_cost
FROM whparisng.plan_table
START WITH id = 0 AND statement_id = '&1'
CONNECT BY PRIOR id = parent_id AND
statement_id = '&1'
order by id
/

select id, object_node, other
from whparisng.plan_table
where statement_id = '&1'
and other is not null
order by id
/

select id, object_node, access_predicates
from whparisng.plan_table
where statement_id = '&1'
and access_predicates is not null
order by id
/

select id, object_node, filter_predicates
from whparisng.plan_table
where statement_id = '&1'
and filter_predicates is not null
order by id
/