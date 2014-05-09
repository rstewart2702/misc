select object_name
from all_objects
where owner = upper('&1')
and object_type = 'PROCEDURE'
order by object_name
/
