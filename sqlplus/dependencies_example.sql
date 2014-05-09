column referenced_type heading 'ref|type'
column dependency_type format a4 heading 'dep|type'
column referenced_link_name format a10 heading 'ref|link|name'
column referenced_name format a25 heading 'referenced|name'
column referenced_owner format a10 heading 'referenced|owner'
column name format a25
column type format a12
column owner format a10

select *
from all_dependencies
where owner =  'SAFNG'
and referenced_owner = 'SAFNG'
-- and (referenced_name like '%_V' or referenced_name like '%_VW')
and referenced_type in ('VIEW','SYNONYM')
order by referenced_name