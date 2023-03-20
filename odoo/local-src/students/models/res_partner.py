from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    ContinuousStudents = fields.One2many(
        string="Continuous Students",
        comodel_name="students.studentcontinuous",
        inverse_name="partner",
    )
