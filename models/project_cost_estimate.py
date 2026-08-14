from odoo import api, fields, models
class ProjectCostEstimate(models.Model):
    _name = "project.cost.estimate"
    _description = "Project Cost app"
    name=fields.Char(string="Project")
    project_id = fields.Many2one("project.project", string="Project")
    breakdown_ids=fields.One2many("project.cost.breakdown","estimate_id",string="Breakdown Items")
    estimated_total_cost=fields.Float(string="Estimated Total Cost",compute="_compute_estimated_total_cost")
    status=fields.Selection([
        ("draft","Draft"),
        ("submitted","Submitted"),
        ("approved","Approved"),
        ("declined","Declined"),
    ],string="Status",default="draft")


    @api.depends("breakdown_ids.subtotal")
    def _compute_estimated_total_cost(self):
        for estimate in self:
            estimate.estimated_total_cost =sum(
                estimate.breakdown_ids.mapped("subtotal")
            )


    def state_action_submit(self):
       for record in self:
          record.status = "submitted"

    def state_action_approve(self):
        for record in self:
            record.status = "approved"

    def state_action_declined(self):
        for record in self:
            record.status = "declined"




