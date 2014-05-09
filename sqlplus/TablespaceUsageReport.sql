/*
  -- 
  -- Tablespace Usage Report
  --
*/
Set Termout Off
Set Echo Off
Set Heading On 
Set Feedback Off 
Set Verify Off
Set Trimspool On
Set Linesize 120
Set Pagesize 100
COLUMN "TBLSPC"  FORMAT A25
COLUMN "ALLOC"   FORMAT 999,999,999,999
COLUMN USED    FORMAT 999,999,999,999
COLUMN UNUSED  FORMAT 999,999,999,999
COLUMN USEDPCT FORMAT 999.99
Set Termout On
Select u.tblspc "TBLSPC"
     , a.fbytes "ALLOC"
     , u.ebytes USED
     , a.fbytes - u.ebytes UNUSED
     , (u.ebytes/a.fbytes) * 100 USEDPCT 
  From (Select tablespace_name tblspc
             , sum(bytes) ebytes 
          From sys.dba_extents
         Group By Tablespace_name) u
     , (Select tablespace_name tblspc
             , sum(bytes) fbytes
          From sys.dba_data_files
         Group By tablespace_name) a
 Where u.tblspc = a.tblspc
/
