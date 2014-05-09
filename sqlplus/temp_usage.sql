COMPUTE sum LABEL 'sum' OF bytes_used ON username
break on username nodup

select (blocks*16384)/1048576 bytes_used, segtype seg_type, v.* from v$tempseg_usage v
order by username, sqlhash, session_num
;
