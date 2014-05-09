set serveroutput on wrapped

declare
  type t_cur is ref cursor;
  --
  lcur_cons t_cur;
  l_tabname varchar2(32) := '&1';
  l_dict_prefix varchar2(4) := '&2';  -- This will be set to 'all_' or 'dba_'.
  --
begin
  if l_dict_prefix = '' then
    l_dict_prefix := 'all_';
  end if;

  open lcur_cons for 
    'select 