from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()

        transactions_vals = []
        for line in self.order_line:
            if not line.product_id.product_tmpl_id.is_prepaid_pack:
                continue

            total_pack_hours = (
                line.product_id.product_tmpl_id.pack_hours * line.product_uom_qty
            )
            product_name = line.product_id.product_tmpl_id.name
            vals = {
                "partner_id": self.partner_id.id,
                "amount": total_pack_hours,
                "description": f"{product_name} - {total_pack_hours} hrs",
                "date": fields.Date.today(),
                "source": "sale_order",
                "transaction_type": "credit",
                "related_sales_order": self.id
            }
            transactions_vals.append(vals)

        if transactions_vals:
            self.env["service.wallet.transaction"].create(transactions_vals)

        return res
