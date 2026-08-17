from odoo import api, fields, models

class ProjectCostBreakdown(models.Model):

    _name="project.cost.breakdown"
    _description = "Items prices"

    name=fields.Char(string="Item")
    quantity=fields.Float(string="Quantity",default=1)
    unit_cost=fields.Float(string="Unit price")
    subtotal=fields.Float(string="Sub Total",compute="_computed_subtotal",store=True)
    estimate_id=fields.Many2one("project.cost.estimate",string="project")

    @api.depends("unit_cost","quantity")
    def _computed_subtotal(self):
        for rec in self:
            rec.subtotal = rec.unit_cost * rec.quantity
