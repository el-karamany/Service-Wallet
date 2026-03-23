from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    
    is_prepaid_pack = fields.Boolean(string='Prepaid Pack', default=False, help="Is this product a support pack?")
    pack_hours = fields.Float(string='Pack Hours', help="How many hours does this pack contain?")