
from ppBackend.scripts.First_Admin_User import create_admin_user_if_not_exists
from ppBackend.scripts.JunkFollowUpLeadHistoryRemoval import junk_follow_up_lead_history_removal
from ppBackend.scripts.Update_id_field import update_id_field
from ppBackend.scripts.phoneNumberFormatCorrection import phone_number_format_correction
from ppBackend.scripts.FindEmptyLeads import find_empty_leads
from ppBackend.scripts.update_leads import update_leads
from ppBackend.scripts.find_missing import find_missing
from ppBackend.scripts.ReportGenerator import Report_Generator


def run_scripts(execute_create_admin_user_if_not_exists=False, execute_phone_number_format_correction=False,
                execute_update_id_field=False, execute_find_empty_leads=False,
                execute_junk_follow_up_lead_history_removal=False, update_leads_execute=False, execute_find_missing=False, 
                execute_report_generator=False):
    create_admin_user_if_not_exists(execute_create_admin_user_if_not_exists)
    phone_number_format_correction(execute_phone_number_format_correction)
    update_id_field(execute_update_id_field)
    find_empty_leads(execute_find_empty_leads)
    junk_follow_up_lead_history_removal(
        execute_junk_follow_up_lead_history_removal)
    update_leads(update_leads_execute)
    find_missing(execute_find_missing)
    Report_Generator(execute_report_generator)