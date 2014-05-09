rem set termout off
rem The following helps us deal with the common ways the connect command
rem is invoked:
rem define 1
rem prompt &1
rem prompt &2
rem prompt &3
connect &1

rem Delete the username/password@instance string from the 
rem SQL*Plus environment (so's the curious won't try to pick it out...)
undefine 1

rem @login
rem set termout on
