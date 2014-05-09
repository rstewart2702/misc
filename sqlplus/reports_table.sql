column rprt_regional_ind format a13 heading 'RPRT|REGIONAL|IND'
column rprt_active_ind format a6 heading 'RPRT|ACTIVE|IND'
column rprt_proc_name format a25 heading 'RPRT|PROC|NAME'
column rprt_proc_param1 format a10 heading 'RPRT|PROC|PARAM1'
column rprt_proc_param2 format a10 heading 'RPRT|PROC|PARAM2'
column rprt_proc_param3 format a10 heading 'RPRT|PROC|PARAM3'

column rprt_al_usage_ind format a6 heading 'RPRT|AL|USAGE|IND'
column rprt_fl_usage_ind format a6 heading 'RPRT|FL|USAGE|IND'
column rprt_ga_usage_ind format a6 heading 'RPRT|GA|USAGE|IND'
column rprt_la_usage_ind format a6 heading 'RPRT|LA|USAGE|IND'
column rprt_ms_usage_ind format a6 heading 'RPRT|MS|USAGE|IND'
column rprt_nc_usage_ind format a6 heading 'RPRT|NC|USAGE|IND'
column rprt_sc_usage_ind format a6 heading 'RPRT|SC|USAGE|IND'
column rprt_tn_usage_ind format a6 heading 'RPRT|TN|USAGE|IND'
column rprt_ky_usage_ind format a6 heading 'RPRT|KY|USAGE|IND'

column rprt_agg_ind format a6 heading 'RPRT|AGG|IND'
column rprt_clec_ind format a6 heading 'RPRT|CLEC|IND'
column rprt_12month_ind format a7 heading 'RPRT|12MONTH|IND'
column rprt_name format a50 trunc
column internal_user format a8 heading 'INTERNAL|USER'
column start_yr_mth_num format 99999999 heading 'START|YR|MTH|NUM'
column end_yr_mth_num format   99999999 heading 'END|YR|MTH|NUM'
column sub_metric_cd format a6 heading 'SUB|METRIC|CD'

select 
  rprt_id
, sbjct_area_cd
, msre_cat_cd
, internal_user
, rprt_active_ind
, rprt_regional_ind
, rprt_al_usage_ind
, rprt_fl_usage_ind
, rprt_ga_usage_ind
, rprt_la_usage_ind
, rprt_ms_usage_ind
, rprt_nc_usage_ind
, rprt_sc_usage_ind
, rprt_tn_usage_ind
, rprt_ky_usage_ind
, rprt_agg_ind
, rprt_clec_ind
, rprt_12month_ind
, rprt_name
, rprt_proc_name
, rprt_proc_param1
, rprt_proc_param2
, rprt_proc_param3
, start_yr_mth_num
, end_yr_mth_num
, sub_metric_cd
from
  &1..reports
where
    sbjct_area_cd = '&&2'
and msre_cat_cd = '&&3'
order by 
  sbjct_area_cd
, msre_cat_cd
, rprt_id
;

