select
  *
from
  (
    select
      l.login_id
    , l.login
    , to_char(l.logindatetime, 'Dy dd-Mon-yyyy hh24:mi:ss') logindatetime
    , u.user_id
    , u.user_type
    from
      pmapwebsrs$.logins l
    , pmapwebsrs.users u
    where
        u.login = l.login
    order by
      l.logindatetime desc
  ) 
where
    rownum <= &1
/
