COLUMN   tb_tpicr_basis_of_cost ON HEADING  'tb_tpicr_|basis_of_cost' headsep '|' FORMAT   a15

COLUMN   rx_origin_code ON HEADING  'rx_origin_|code' headsep '|' FORMAT   a15

COLUMN   rtp_reprint_label ON HEADING  'rtp_reprint_|label' headsep '|' FORMAT   a15

COLUMN   medicare_patient_location_code ON HEADING  'medicare_|patient_|location_code' headsep '|' FORMAT   a15

COLUMN   emergency_condition_code ON HEADING  'emergency_|condition_|code' headsep '|' FORMAT   a15

COLUMN   medicare_assignment_indicator ON HEADING  'medicare_|assignment_|indicator' headsep '|' FORMAT   a15

COLUMN   product_id_override ON HEADING  'product_|id_override' headsep '|' FORMAT   a15

COLUMN   external_billing_indicator ON HEADING  'external_|billing_|indicator' headsep '|' FORMAT   a10

COLUMN   manual_reversal_indicator ON HEADING  'manual_|reversal_|indicator' headsep '|' FORMAT   a10

COLUMN   billing_status ON HEADING  'billing_|status' headsep '|' FORMAT   a10

COLUMN   processing_status ON HEADING  'processing_|status' headsep '|' FORMAT   a15

COLUMN   comments_problem ON FORMAT   a25 wrap 

COLUMN   comments_consulted ON FORMAT   a25 wrap 

COLUMN   comments_result ON FORMAT   a25 wrap 

COLUMN   comments_user ON FORMAT   a25 wrap 

COLUMN   clm_sumry_override_data ON FORMAT   a25 wrap 

COLUMN   internal_fill_id ON FORMAT   99999999999999999

COLUMN   rxf_rx_record_num ON FORMAT   99999999999999999

COLUMN   tp_item_claim_result_num ON FORMAT   99999999999999999

COLUMN   price_calc_result_num ON FORMAT   99999999999999999

COLUMN   item_price_calc_result_num ON FORMAT   99999999999999999

COLUMN   item_seq ON FORMAT   99999999999999999

COLUMN   order_num ON FORMAT   99999999999999999

COLUMN   tp_item_claim_num ON FORMAT   99999999999999999

COLUMN   reassigned_rx_num ON FORMAT   99999999999999999

COLUMN   rx_fill_seq ON FORMAT   99999999999999999

COLUMN   io_cost ON FORMAT   9999999

COLUMN   cpu_cost ON FORMAT   9999999

COLUMN   temp_space ON FORMAT   9999999

COLUMN   filter_predicates ON HEADING  'filter|predicates' headsep '|' FORMAT   a85 wrap 

COLUMN   access_predicates ON HEADING  'access|predicates' headsep '|' FORMAT   a85 wrap 

COLUMN   partition_id ON HEADING  'prtn|id' headsep '|' FORMAT   9999

COLUMN   partition_stop ON HEADING  'prtn|stop' headsep '|' FORMAT   a15 JUSTIFY left word_wrap 

COLUMN   partition_start ON HEADING  'prtn|start' headsep '|' FORMAT   a15 JUSTIFY left word_wrap 

COLUMN   distribution ON FORMAT   a20

COLUMN   optimizer ON FORMAT   a12 JUSTIFY left 

COLUMN   position ON HEADING  'posi-|tion' headsep '|' FORMAT   9999999 JUSTIFY right 

COLUMN   other_tag ON HEADING  'OTHER_TAG' FORMAT   a29 JUSTIFY left wrap 

COLUMN   object_node ON FORMAT   a15

COLUMN   other ON FORMAT   a85

COLUMN   options ON FORMAT   a10 word_wrap 

COLUMN   operation ON FORMAT   a150 wrap 

COLUMN   object_name ON FORMAT   a20 wrap 

COLUMN   parent_id ON HEADING  'par|id' headsep '|' FORMAT   999

COLUMN   id ON HEADING  'id' FORMAT   999

COLUMN   isprimary ON HEADING  'IS|PRIMARY' headsep '|' FORMAT   a10

COLUMN   ISBUSINESSBILLINGADDRESS ON HEADING  'IS|BUSINESS|BILLING|ADDRESS' headsep '|' FORMAT   A15

COLUMN   ISALTBUSINESSCONTACT ON HEADING  'IS|ALT|BUSINESS|CONTACT' headsep '|' FORMAT   A15

COLUMN   isresponsibleperson ON HEADING  'IS|RESPONSIBLE|PERSON' headsep '|' FORMAT   a15

COLUMN   nice_title ON FORMAT   a40

COLUMN   erx_client_id ON FORMAT   a8

COLUMN   name ON FORMAT   a20

COLUMN   override_name ON FORMAT   a15

COLUMN   data_map_name ON FORMAT   a50 truncate 

COLUMN   externalbillingindicator ON HEADING  'external|billing|indicator' headsep '|' FORMAT   a11

COLUMN   manualreversalindicator ON HEADING  'manual|reversal|indicator' headsep '|' FORMAT   a11

COLUMN   billingstatus ON HEADING  'billing|status' headsep '|' FORMAT   a11

COLUMN   processingstatus ON HEADING  'processing|status' headsep '|' FORMAT   a11

COLUMN   tp_sel2_plan_sel2_mapkey ON HEADING  'tp_sel2_|plan_sel2_|mapkey' headsep '|' FORMAT   a10

COLUMN   tp_sel2_plan_sel1_plancode ON HEADING  'tp_sel2_|plan_sel1_|plancode' headsep '|'FORMAT   a10

COLUMN   tp_sel2_plan_sel ON HEADING  'tp_sel2_|plan_sel' headsep '|' FORMAT   a8

COLUMN   tp_sel1_cardid ON HEADING  'tp_sel1_|cardid' headsep '|' FORMAT   a20

COLUMN   tp_sel ON HEADING  'tp_|sel' headsep '|' FORMAT   a3

COLUMN   thirdpartyplan_sel2_mapkey ON HEADING  'thirdpartyplan_|sel2_mapkey' headsep '|' FORMAT   a20

COLUMN   thirdpartyplan_sel1_plancode ON HEADING  'thirdpartyplan_|sel1_plancode' headsep '|' FORMAT   a20

COLUMN   thirdpartyplan_sel ON HEADING  'third|party|plan_sel' headsep '|' FORMAT   a10

COLUMN   rprt_proc_param3 ON HEADING  'rprt_|proc_|param3' headsep '|' FORMAT   a10

COLUMN   rprt_proc_param2 ON HEADING  'rprt_|proc_|param2' headsep '|' FORMAT   a10

COLUMN   rprt_proc_param1 ON HEADING  'rprt_|proc_|param1' headsep '|' FORMAT   a10

COLUMN   rprt_12month_ind ON HEADING  'rprt_|12month_|ind' headsep '|' FORMAT   a8

COLUMN   rprt_type ON HEADING  'rprt_|type' headsep '|' FORMAT   a6

COLUMN   internal_user ON HEADING  'internal_|user' headsep '|' FORMAT   a10

COLUMN   rprt_regional_ind ON HEADING  'rprt_|regional_|ind' headsep '|' FORMAT   a12

COLUMN   rprt_active_ind ON HEADING  'rprt_|active_|ind' headsep '|' FORMAT   a8

COLUMN   rprt_clec_ind ON HEADING  'rprt_|clec_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_agg_ind ON HEADING  'rprt_|agg_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_tn_usage_ind ON HEADING  'rprt_|tn_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_sc_usage_ind ON HEADING  'rprt_|sc_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_nc_usage_ind ON HEADING  'rprt_|nc_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_ms_usage_ind ON HEADING  'rprt_|ms_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_la_usage_ind ON HEADING  'rprt_|la_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_ky_usage_ind ON HEADING  'rprt_|ky_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_ga_usage_ind ON HEADING  'rprt_|ga_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_fl_usage_ind ON HEADING  'rprt_|fl_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   rprt_al_usage_ind ON HEADING  'rprt_|al_|usage_|ind' headsep '|' FORMAT   a6

COLUMN   region_plan_2005_ind ON HEADING  'region|plan|2005|ind' headsep '|' FORMAT   a6

COLUMN   remove_bcv_ind ON HEADING  'remove|bcv|ind' headsep '|' FORMAT   a6

COLUMN   msre_based_plan_ind ON HEADING  'msre|based|plan|ind' headsep '|' FORMAT   a6

COLUMN   parent_cmpny_rollup_ind ON HEADING  'parent|cmpny|rollup|ind' headsep '|' FORMAT   a6

COLUMN   psc_interest_ind ON HEADING  'psc|interest|ind' headsep '|' FORMAT   a8

COLUMN   rolng_qtr ON HEADING  'rolng|qtr' headsep '|' FORMAT   a5

COLUMN   rmdy_int_type_cd ON HEADING  'rmdy|int|type|cd' headsep '|' FORMAT   a4

COLUMN   rmdy_unit_mnl_ind ON HEADING  'rmdy_|unit_|mnl_|ind' headsep '|' FORMAT   a6

COLUMN   re_run_overwrite_flg ON HEADING  're_run_|overwrite_|flg' headsep '|' FORMAT   a9

COLUMN   rmdy_status_rsn_cd ON HEADING  'rmdy_|status_|rsn_|cd' headsep '|' FORMAT   a8

COLUMN   rmdy_unit_sts_cd ON HEADING  'rmdy_|unit_|sts_|cd' headsep '|' FORMAT   a8

COLUMN   rmdy_unit_src_cd ON HEADING  'rmdy_|unit_|src_|cd' headsep '|' FORMAT   a8

COLUMN   rmdy_tran_type_cd ON HEADING  'rmdy_|tran_|type_|cd' headsep '|' FORMAT   a8

COLUMN   rmdy_unit_type_cd ON HEADING  'rmdy_|unit_|type_|cd' headsep '|' FORMAT   a8

COLUMN   rmdy_unit_rsn_cd ON HEADING  'rmdy_|unit_|rsn_cd' headsep '|' FORMAT   a8

COLUMN   prod_grp_bst_desc ON FORMAT   a20 wrap 

COLUMN   prod_grp_clec_desc ON FORMAT   a20 wrap 

COLUMN   prod_grp_desc ON FORMAT   a80 wrap 

COLUMN   subm_desc ON FORMAT   a80 wrap 

COLUMN   this_day ON NEW_VALUE TODAY_DATE

COLUMN   global_name ON NEW_VALUE GNAME

COLUMN   column_name ON FORMAT   a40 wrap 

COLUMN   endpoint_actual_value ON FORMAT   a50 wrap 

COLUMN   table_name ON FORMAT   a30 wrap 

COLUMN   table_owner ON FORMAT   a30 wrap 

COLUMN   synonym_name ON FORMAT   a30 wrap 

COLUMN   db_link ON FORMAT   a40 wrap 

COLUMN   other_plus_exp ON FORMAT   a100

COLUMN   other_tag_plus_exp ON FORMAT   a29

COLUMN   object_node_plus_exp ON FORMAT   a15

COLUMN   plan_plus_exp ON FORMAT   a110

COLUMN   parent_id_plus_exp ON HEADING  'p' FORMAT   990

COLUMN   id_plus_exp ON HEADING  'i' FORMAT   990

COLUMN   value_col_plus_show_param ON HEADING  'VALUE' FORMAT   a30

COLUMN   name_col_plus_show_param ON HEADING  'NAME' FORMAT   a36

COLUMN   name_col_plus_show_sga ON FORMAT   a24

COLUMN   ERROR ON FORMAT   A65 word_wrap 

COLUMN   LINE/COL ON FORMAT   A8

COLUMN   ROWLABEL ON FORMAT   A15

column is_cash heading 'is_|cash' format a5
column is_refill heading 'is_|refill' format a8
column daw_code heading 'daw_|code' format a6
column short_fill_status heading 'short_|fill_|status' format a8
column is_paid heading 'is_|paid' format a6
column tp_item_claim_exists heading 'tp_item_|claim_exists' format a15
column tpic_rx_origin_code heading 'tpic_rx_|origin_code' format a15
column rxdx_rx_origin_code heading 'rxdx_rx_|origin_code' format a15
column cash_price_exists heading 'cash_price_|exists' format a15
column claim_summary_price_exists heading 'claim_summary_|price_exists' format a20
column basis_of_cost heading 'basis_of_|cost' format a15
column txn_type heading 'txn_|type' format a10
column patient_pay_src heading 'patient_|pay_src' format a10
column price_override_rsn_code heading 'price_override_|rsn_code' format a20
column result format a10
column comments_problem_exists heading 'comments_problem_|exists' format a20
column cai_rx_origin_code heading 'cai_rx_origin_|code' format a20
column cai_cash_info_exists heading 'cai_cash_info_|exists' format a20
column comments_consulted_exists heading 'comments_|consulted_exists' format a20
column comments_result_exists heading 'comments_result_|exists' format a20
column comments_problem heading 'comments_|problem' format a10
column comments_user_exists heading 'comments_user_|exists' format a20
column directions format a25 wrap
column status format a10 wrap
column is_compound heading 'is_|compound' format a8
