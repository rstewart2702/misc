column dependency format a80 wrapped
column dep_level format 999999999
column object_name format a40 wrapped
column object_type format a20 wrapped
column nametype noprint
break on nametype skip 1
rem break on name skip 0 on type skip 1
set verify off

prompt WHAT &1..&2 DEPENDS ON:

select
  owner, object_name, object_type
from
  dba_objects
where owner = upper('&1') and object_name = upper('&2')
;

rem select 
rem   owner, name, type
rem from dba_dependencies
rem where owner = upper('&1') and name = upper('&2')
rem ;

select
  *
from
  (
    select 
      decode(prior name, null, name, prior name) name
    , decode(prior type, null, type, prior type) type
    , level dep_level
    -- , lpad(' ', 2*(level - 1))||owner||'.'||name||' ('||type||')' info
    , lpad(' ', 2*(level - 1))||referenced_owner||'.'||referenced_name||
        decode(referenced_link_name,
                 null,         ' ('||referenced_type||')',
                 /* default */ '@'||referenced_link_name||' (REMOTE '||referenced_type||')'
              )
        dependency
    , decode(prior name, null, name, prior name)||decode(prior type, null, type, prior type) nametype
    from
      dba_dependencies
    start with
        owner = upper('&1')
    and name = upper('&2')
    connect by
        name = prior referenced_name
    and owner = prior referenced_owner
    and type = prior referenced_type
    order siblings by referenced_name, referenced_type, level
  )
-- order by name, type, level
/

rem select 
rem   level dep_level
rem -- , lpad(' ', 2*(level - 1))||owner||'.'||name||' ('||type||')' info
rem , lpad(' ', 2*(level - 1))||referenced_owner||'.'||referenced_name||
rem     decode(referenced_link_name,
rem              null,         ' ('||referenced_type||')',
rem              /* default */ '@'||referenced_link_name||' (REMOTE '||referenced_type||')'
rem           )
rem     dependency
rem from
rem   dba_dependencies
rem start with
rem     owner = 'PARISNG$'
rem and name = 'AUDIT_CONTROL'
rem and type = 'PACKAGE BODY'
rem connect by
rem     name = prior referenced_name
rem and owner = prior referenced_owner
rem and type = prior referenced_type
