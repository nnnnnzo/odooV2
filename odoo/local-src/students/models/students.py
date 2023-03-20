from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StudentsTraining(models.Model):
    _name = "students.training"
    _description = "Training table"
    _rec_name = "code"
    code = fields.Char(string="Training code", size=4, required=True)
    name = fields.Char(string="Training name", size=100, required=True)
    student_ids = fields.One2many(
        string="Training students",
        comodel_name="students.student",
        inverse_name="training_id",
    )
    # @api.constrains('code')
    # def _check_code(self):
    #     for record in self:
    #         if self.env['students.training'].search([('code', '=', record.code)]):
    #             raise ValidationError("Training code already exists, it must be unique")

class StudentsMark(models.Model):
    _name = "students.mark"
    _description = "Mark table"
    subject = fields.Char(string="Mark subject", size=50, required=True)
    mark = fields.Float(string="Mark", required=True)
    coefficient = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('5', '5')
    ], string='Coefficient', required=True, help="Select a coefficient in the list", index=True, default='1')
    coefMark = fields.Float(compute='_compute_mark', string="Weighted Mark")
    @api.depends('mark', 'coefficient')
    def _compute_mark(self):
        for record in self:
            record.coefMark = record.mark * float(record.coefficient)

    student_ids = fields.Many2one(
        string="Student",
        comodel_name="students.student",
        ondelete="cascade",
        required=True,
    )
    @api.constrains('mark')
    def _check_mark(self):
        for record in self:
            if record.mark > 20 or record.mark < 0:
                raise ValidationError("Mark must be between 0 and 20")


class StudentsStudent(models.Model):
    _name = "students.student"
    _description = "Student table"
    ##_rec_name = "number"

    number = fields.Char("Student number", size=11, required=True)
    firstname = fields.Char("Student firstname", size=64, required=True)
    lastname = fields.Char("Student lastname", size=64, required=True)
    training_id = fields.Many2one(
        string="Training",
        comodel_name="students.training",
        ondelete="cascade",
    )
    mark_ids = fields.One2many(
        string="Student Marks",
        comodel_name="students.mark",
        inverse_name="student_ids",
    )
    country = fields.Many2one(
        string="Student Country",
        comodel_name="res.country",
        ondelete="cascade",
    )
    avgMark = fields.Float(compute='_compute_avg', string="Grade point average")
    @api.depends('mark_ids')
    def _compute_avg(self):
        coefTT = 0
        for record in self:
            if len(record.mark_ids) > 0:
                for m in record.mark_ids:
                    record.avgMark += m.coefMark
                    coefTT += float(m.coefficient)
                record.avgMark = record.avgMark / coefTT
            else:
                record.avgMark = 0

    def name_get(self):
        result = []
        for record in self:
            name = record.firstname + ' ' + record.lastname
            result.append((record.id, name))
        return result
class StudentsStudentContinious(models.Model):
    _name = "students.studentcontinuous"
    _inherit = "students.student"
    _description = "StudentContinuous table"
    partner = fields.Many2one(
        string="Company",
        comodel_name="res.partner",
        ondelete="cascade",
    )