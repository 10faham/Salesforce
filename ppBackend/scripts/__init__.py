
from ppBackend.scripts.First_Admin_User import create_admin_user_if_not_exists
from ppBackend.scripts.Update_id_field import update_id_field
from ppBackend.scripts.phoneNumberFormatCorrection import phone_number_format_correction
from ppBackend.scripts.FindEmptyLeads import find_empty_leads


def run_scripts(execute_create_admin_user_if_not_exists=False, execute_phone_number_format_correction=False, execute_update_id_field=False, execute_find_empty_leads = False):
    create_admin_user_if_not_exists(execute_create_admin_user_if_not_exists)
    phone_number_format_correction(execute_phone_number_format_correction)
    update_id_field(execute_update_id_field)
    find_empty_leads(execute_find_empty_leads)
