select view_name
from all_views
where owner = upper('&1')
order by view_name
/
