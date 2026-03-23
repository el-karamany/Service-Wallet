from odoo import models, fields, api


class ServiceWalletTransaction(models.Model):
    _name = "service.wallet.transaction"
    _description = "Service Wallet Transaction"

    partner_id = fields.Many2one("res.partner", string="Partner", index=True, readonly=True)
    amount = fields.Float(string="Amount", readonly=True)
    description = fields.Char(string="Description", readonly=True)
    date = fields.Date(string="Date", readonly=True)
    source = fields.Selection([("sale_order", "Sales Order"), ("manual", "Manual (Log Support)")], string="Source", readonly=True)
    transaction_type = fields.Selection([("credit", "Credit"), ("debit", "Debit")], string="Transaction Type", readonly=True)
    related_sales_order = fields.Many2one("sale.order", string="Related Sales Order", readonly=True)
