from odoo import models,fields

class ProjectInfoWizard(models.TransientModel):
    _name = "project.info.wizard"
    _description = "Project Information Wizard"

    # name = fields.Char(string="Name")
    start_date = fields.Date(string="Start date", required=True)
    end_date = fields.Date(string="End date")