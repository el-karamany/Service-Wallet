from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    remaining_hours = fields.Float(
        string="Remaining Hours", compute="_compute_remaining_hours"
    )
    transaction_count = fields.Integer(compute="_compute_transaction_count")
    transaction_ids = fields.One2many("service.wallet.transaction", "partner_id")

    @api.depends("transaction_ids.amount", "transaction_ids.transaction_type")
    def _compute_remaining_hours(self):
        transactions = self.env["service.wallet.transaction"].sudo().read_group(
            [("partner_id", "in", self.ids)],
            ["partner_id", "transaction_type", "amount:sum"],
            ["partner_id", "transaction_type"],
            lazy=False
        )
        data = {}
        for t in transactions:
            pid = t["partner_id"][0]
            data.setdefault(pid, {"credit": 0.0, "debit": 0.0})
            data[pid][t["transaction_type"]] = t["amount"]
            
            
        for partner in self:
            d = data.get(partner.id, {})
            partner.remaining_hours = d.get("credit", 0.0) - d.get("debit", 0.0)


    @api.depends("transaction_ids")
    def _compute_transaction_count(self):
        counts = self.env["service.wallet.transaction"].sudo().read_group(
            [("partner_id", "in", self.ids)], ["partner_id"], ["partner_id"]
        )
        count_map = {r["partner_id"][0]: r["partner_id_count"] for r in counts}
        for partner in self:
            partner.transaction_count = count_map.get(partner.id, 0)

    def action_view_wallet_transactions(self):
        """This method is triggered when the button is clicked"""
        self.ensure_one()
        return {
            "name": "Wallet Transactions",
            "type": "ir.actions.act_window",
            "res_model": "service.wallet.transaction",
            "view_mode": "tree",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
            "target": "current",
        }
