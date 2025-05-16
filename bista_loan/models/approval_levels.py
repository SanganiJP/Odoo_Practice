from odoo import fields, models, api


class ApprovalLevels(models.Model):
    _name = 'approval.levels'
    _description = 'Description'


    team_id = fields.Many2one('loan.approval.team', string="Team Name")
    name = fields.Char(string="Approval Level")
    team_member = fields.Many2many('res.users',string="Team Member")
    team_level = fields.Integer(compute='_compute_level', string="Level", store=True)

    @api.depends('team_id.approval_level_ids')
    def _compute_level(self):
        for rec in self:
            team_level = 0
            # team_rec = self.env['loan.approval.team'].search([('name','=',rec._origin.name)])
            # level = len(team_rec)
            rec.team_level = team_level
            for level in rec.team_id.approval_level_ids:
                team_level += 1
                level.team_level = team_level

