from odoo import models, fields, api
# access_user_ds_medical_treatment,access_user_ds_medical_treatment,model_ds_medical_treatment,ds_hospital_base.group_hospital_access_user,1,0,0,0
# access_spv_ds_medical_treatment,access_spv_ds_medical_treatment,model_ds_medical_treatment,ds_hospital_base.group_hospital_access_spv,1,1,1,0
# access_manager_ds_medical_treatment,access_manager_ds_medical_treatment,model_ds_medical_treatment,ds_hospital_base.group_hospital_access_manager,1,1,1,1

class DsMedicalTreatment(models.Model):
    _name = 'ds.medical.treatment'
    _description = 'Medical Treatment'

    
