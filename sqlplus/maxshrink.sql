rem 01-23-2003
rem VERY useful script from Tom Kyte's website;
rem this script attempts to identify whether or not
rem it's possible to shrink the datafiles used by
rem your database instance. It runs a query to
rem show where the savings might be made, and then
rem generates the commands necessary to make Oracle
rem resize the datafile.
rem
set verify off
column file_name format a50 word_wrapped
column smallest format 9,999,990 heading "Smallest|Size|Possible"
column currsize format 999,990 heading "Current|Size"
column savings  format 9,999,990 heading "Possible|Savings"
break on report
compute sum of savings on report

column value new_val blksize
select value from v$parameter where name = 'db_block_size'
/

select file_name,
       ceil( (nvl(hwm,1)*&&blksize)/1024/1024 ) smallest,
       ceil( blocks*&&blksize/1024/1024) currsize,
       ceil( blocks*&&blksize/1024/1024) -
       ceil( (nvl(hwm,1)*&&blksize)/1024/1024 ) savings
from dba_data_files a,
     ( select file_id, max(block_id+blocks-1) hwm
         from dba_extents
        group by file_id ) b
where a.file_id = b.file_id(+)
/

column cmd format a75 word_wrapped

select 'alter database datafile '''||file_name||''' resize ' ||
       ceil( (nvl(hwm,1)*&&blksize)/1024/1024 )  || 'm;' cmd
from dba_data_files a,
     ( select file_id, max(block_id+blocks-1) hwm
         from dba_extents
        group by file_id ) b
where a.file_id = b.file_id(+)
  and ceil( blocks*&&blksize/1024/1024) -
      ceil( (nvl(hwm,1)*&&blksize)/1024/1024 ) > 0
/
