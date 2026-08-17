from odoo import api, fields, models


class ProjectCostEstimate(models.Model):
    _name = "project.cost.estimate"
    _description = "Project Cost app"
    name=fields.Char(string="Project")
    project_id = fields.Many2one("project.project", string="Project from projects")
    breakdown_ids=fields.One2many("project.cost.breakdown","estimate_id",string="Breakdown Items")
    currency_id=fields.Many2one("res.currency",string="Currency")
    estimated_total_cost=fields.Monetary(string="Estimated Total Cost",compute="_compute_estimated_total_cost")
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
            template = self.env.ref(
                "project_cost.email_template_cost_estimate_approved"
            )
            if record.create_uid.email:
                template.send_mail(
                    record.id,
                    force_send=True,
                    email_values={
                        "email_to": record.create_uid.email,
                    },
                )

    def state_action_declined(self):
        for record in self:
            record.status = "declined"

            template = self.env.ref(
                "project_cost.email_template_cost_estimate_declined"
            )

            if record.create_uid.email:
                template.send_mail(
                    record.id,
                    force_send=True,
                    email_values={
                        "email_to": record.create_uid.email,
                    },
                )
    def state_action_draft(self):
        for record in self:
            record.status = "draft"




