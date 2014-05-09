set serveroutput on size 1000000 format wrapped

set trimspool on
set trimout on
set long 5000
set linesize 1000
rem set pagesize 9999
set pagesize 32767
rem SET THE COLUMN SEPARATOR TO A TAB CHARACTER (MAKES COPYING INTO SPREADSHEET PROGRAMS EASIER...)
set colsep '	'

rem These column definitions come in handy when we perform an autotrace.
rem They help make the output of autotrace a little easier to read.
rem
rem column plan_plus_exp format a200
column plan_plus_exp format a110
rem
rem column other_plus_exp format a100
column other_plus_exp format a100
rem
column object_node_plus_exp format a15

rem These are common data dictionary column settings:
column db_link format a40 wrapped
column synonym_name format a30 wrapped
column table_owner format a30 wrapped
column table_name format a30 wrapped
column endpoint_actual_value format a50 wrapped
column column_name format a40 wrapped

rem Define the gname &-substitution variable so that we won't be prompted
rem for it later, in case Oracle doesn't have an instance mounted yet.
define gname='NO_ORACLE'
column global_name new_value gname
set termout off
rem set echo on

select lower(user) || '@' ||
       decode(global_name, 'ORACLE8.WORLD', '8.0', 'ORA8I.WORLD', '8i', global_name) global_name 
from global_name;
set sqlprompt '&gname> '
set termout on

set termout off
alter session set nls_date_format = 'DD-MON-YYYY HH24:MI:SS';
set termout on

define today_date='DID NOT FETCH DATE'
column this_day new_value today_date
set termout off
select to_char(sysdate,'Dy dd-mon-yyyy hh:mi:ss am') this_day from dual;
set termout on
prompt Logged in at: &today_date
undefine today_date
prompt


rem General column format settings for some commonly viewed columns in PARIS:
column subm_desc format a80 wrapped
column prod_grp_desc format a80 wrapped
column prod_grp_clec_desc format a20 wrapped
column prod_grp_bst_desc format a20 wrapped

rem Some column format settings for columns which come up in remedy queries:
column rmdy_unit_rsn_cd format a8 heading 'rmdy_|unit_|rsn_cd'
column rmdy_unit_type_cd format a8 heading 'rmdy_|unit_|type_|cd'
column rmdy_tran_type_cd format a8 heading 'rmdy_|tran_|type_|cd'
column rmdy_unit_src_cd format a8 heading 'rmdy_|unit_|src_|cd'
column rmdy_unit_sts_cd format a8 heading 'rmdy_|unit_|sts_|cd'
column rmdy_status_rsn_cd format a8 heading 'rmdy_|status_|rsn_|cd'
column re_run_overwrite_flg format a9 heading 're_run_|overwrite_|flg'
column rmdy_unit_mnl_ind format a6 heading 'rmdy_|unit_|mnl_|ind'

rem These are columns from the state_ap_cntrl table:
column rmdy_int_type_cd format a4 heading 'rmdy|int|type|cd'
column rolng_qtr format a5 heading 'rolng|qtr'
column psc_interest_ind format a8 heading 'psc|interest|ind'
column parent_cmpny_rollup_ind format a6 heading 'parent|cmpny|rollup|ind'
column msre_based_plan_ind format a6 heading 'msre|based|plan|ind'
column remove_bcv_ind format a6 heading 'remove|bcv|ind'
column region_plan_2005_ind format a6 heading 'region|plan|2005|ind'

rem These columns are for the web-reporting table named REPORTS:
column rprt_al_usage_ind format a6 heading 'rprt_|al_|usage_|ind'
column rprt_fl_usage_ind format a6 heading 'rprt_|fl_|usage_|ind'
column rprt_ga_usage_ind format a6 heading 'rprt_|ga_|usage_|ind'
column rprt_ky_usage_ind format a6 heading 'rprt_|ky_|usage_|ind'
column rprt_la_usage_ind format a6 heading 'rprt_|la_|usage_|ind'
column rprt_ms_usage_ind format a6 heading 'rprt_|ms_|usage_|ind'
column rprt_nc_usage_ind format a6 heading 'rprt_|nc_|usage_|ind'
column rprt_sc_usage_ind format a6 heading 'rprt_|sc_|usage_|ind'
column rprt_tn_usage_ind format a6 heading 'rprt_|tn_|usage_|ind'
column rprt_agg_ind format a6 heading 'rprt_|agg_|ind'
column rprt_clec_ind format a6 heading 'rprt_|clec_|ind'
column rprt_active_ind format a8 heading 'rprt_|active_|ind'
column rprt_regional_ind format a12 heading 'rprt_|regional_|ind'
column internal_user format a10 heading 'internal_|user'
column rprt_type format a6 heading 'rprt_|type'
column rprt_12month_ind format a8 heading 'rprt_|12month_|ind'
column rprt_proc_param1 format a10 heading 'rprt_|proc_|param1'
column rprt_proc_param2 format a10 heading 'rprt_|proc_|param2'
column rprt_proc_param3 format a10 heading 'rprt_|proc_|param3'

rem These column definitions are EnterpriseRx-specific.
rem First, columns for stage_tp_patient (3rd-party card table):
column thirdpartyplan_sel format a10 heading 'third|party|plan_sel'
column thirdpartyplan_sel1_plancode format a20 heading 'thirdpartyplan_|sel1_plancode'
column thirdpartyplan_sel2_mapkey format a20 heading 'thirdpartyplan_|sel2_mapkey'
rem
rem Columns from the stage_claim records, which are the CLAIM-typed, which end up in trexone_data.tp_item_claim, I believe:
column tp_sel format a3 heading 'tp_|sel'
column tp_sel1_cardid format a20 heading 'tp_sel1_|cardid'
column tp_sel2_plan_sel format a8 heading 'tp_sel2_|plan_sel'
column tp_sel2_plan_sel1_plancode format a10 heading 'tp_sel2_|plan_sel1_|plancode'
column tp_sel2_plan_sel2_mapkey format a10 heading 'tp_sel2_|plan_sel2_|mapkey'
column processingstatus format a11 heading 'processing|status'
column billingstatus format a11 heading 'billing|status'
column manualreversalindicator format a11 heading 'manual|reversal|indicator'
column externalbillingindicator format a11 heading 'external|billing|indicator'

rem Some more column defn's, just in case, for McKesson Stuff:
column data_map_name format a50 trunc
column override_name format a15
column name format a20
column erx_client_id format a8
column nice_title format a40
column isresponsibleperson format a15 heading 'IS|RESPONSIBLE|PERSON'
COLUMN ISALTBUSINESSCONTACT FORMAT A15 HEADING 'IS|ALT|BUSINESS|CONTACT'
COLUMN ISBUSINESSBILLINGADDRESS FORMAT A15 HEADING 'IS|BUSINESS|BILLING|ADDRESS'
column isprimary format a10 heading 'IS|PRIMARY'
column isprimary format a10 heading 'IS|PRIMARY'

@setup_columns.sql

set numwidth 15
set timing on
set tab off
