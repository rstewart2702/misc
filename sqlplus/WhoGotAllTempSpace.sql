--
-- To query who got all the temporary tablespace
--
Set LineSize 500
   Select b.tablespace
        , b.segfile#
        , b.segblk#
        , round(((b.blocks*p.value)/1024/1024),2) size_mb
        , a.sid
        , a.serial#
        , a.username
        , a.osuser
        , a.program
        , a.status
     From v$session a
        , v$sort_usage b
        , v$process c
        , v$parameter p
    Where p.name  = 'db_block_size' 
      And a.saddr = b.session_addr  
      And a.paddr=c.addr
    Order By b.tablespace
           , b.segfile#
           , b.segblk#
           , b.blocks
/           

Set LineSize 80
