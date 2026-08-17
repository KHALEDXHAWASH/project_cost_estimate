from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    cost_estimate_ids = fields.One2many(
        "project.cost.estimate",
        "project_id",
        string="Cost Estimates"
    )

    cost_estimate_count = fields.Integer(
        string="Cost Estimates",
        compute="_compute_cost_estimate_count"
    )

    latest_cost_estimate_id = fields.Many2one(
        "project.cost.estimate",
        string="Latest Cost Estimate",
        compute="_compute_latest_cost_estimate"
    )

    latest_cost = fields.Float(
        string="Latest Cost",
        compute="_compute_latest_cost_estimate"
    )

    @api.depends("cost_estimate_ids")
    def _compute_cost_estimate_count(self):
        for project in self:
            project.cost_estimate_count = len(
                project.cost_estimate_ids
            )

    @api.depends(
        "cost_estimate_ids",
        "cost_estimate_ids.create_date"
    )
    def _compute_latest_cost_estimate(self):
        for project in self:
            latest = self.env["project.cost.estimate"].search(
                [
                    ("project_id", "=", project.id)
                ],
                order="create_date desc",
                limit=1
            )

            project.latest_cost_estimate_id = latest

            if latest:
                project.latest_cost = latest.estimated_total_cost
            else:
                project.latest_cost = 0.0

    def action_view_cost_estimates(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Cost Estimates",
            "res_model": "project.cost.estimate",
            "view_mode": "list,form,kanban",
            "domain": [
                ("project_id", "=", self.id)
            ],
            "context": {
                "default_project_id": self.id,
            },
        }