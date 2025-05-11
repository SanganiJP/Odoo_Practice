# -*- encoding: utf-8 -*-

from odoo import fields, models


class Lead(models.Model):
    _name = "lead.info"
    _description = "Lead Information"

    name = fields.Char(string="Project Lead")
    lead_ids = fields.One2many("project.detail", 'project_lead_name', string='Lead Data')
    project_ids = fields.Many2many("res.users", "rel_res_users", column1="project_detail_id", column2="res_users_id",
                                   string="Users")
    project_users = fields.Many2many("res.users", "rel_res_ids", column1="project_users_id", column2="res_users_ids",
                                     string="Users Selection")
    opening_date = fields.Date(string="Starting Date")

    def action_project_info_wizard(self):
        view_id = self.env.ref('project_management.project_info_wizard_wizard').id
        print("view_id", view_id)

        return {
            'name': 'Starting Date',
            'view_mode': 'form',
            'res_model': 'project.info.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
