from odoo import models, fields
from odoo.exceptions import UserError


class LogSupportWizard(models.TransientModel):
    _name = "log.support.wizard"
    _description = "Log Support Wizard"

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    description = fields.Char(string="Description", required=True)
    hours_spent = fields.Float(string="Hours Spent", required=True)

    def action_confirm(self):
        if self.hours_spent > self.partner_id.remaining_hours:
            raise UserError(
                f"Insufficient balance. "
                f"{self.partner_id.name} has {self.partner_id.remaining_hours} hrs remaining, "
                f"but you're trying to log {self.hours_spent} hrs."
            )

        self.env["service.wallet.transaction"].create(
            {
                "partner_id": self.partner_id.id,
                "amount": self.hours_spent,
                "description": self.description,
                "date": fields.Date.today(),
                "source": "manual",
                "transaction_type": "debit",
            }
        )

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
