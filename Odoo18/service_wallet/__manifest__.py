# -*- coding: utf-8 -*-
{
    'name': 'Service Wallet',
    'version': '18.0.0.1.0',
    'summary': 'Manage prepaid support hour packs and customer service wallets',
    'description': """
        Service Wallet
        ==============
        Allows IT consultancies to sell prepaid support hour packs to clients and track consumption.

        Features:
        - Mark products as prepaid support packs with configurable hours
        - Automatically credit customer wallet upon Sales Order confirmation
        - Full transaction history per customer (credits & debits)
        - Log Support wizard to deduct hours with insufficient balance protection
        - Wallet visibility restricted to authorized users
    """,
    'author': 'Omar El-Karamany',
    'website': 'https://github.com/el-karamany/Service-Wallet.git',
    'category': 'Sales',
    'depends': ['base', 'sale', 'product', 'contacts'],
    "data": [
        
        # Security
        "security/groups.xml",
        "security/ir.model.access.csv",
        
        # Views
        "views/res_partner_views.xml",
        "views/service_wallet_transaction_views.xml",
        "views/product_template_views.xml",
        
        # wizard
        "wizard/log_support_wizard_views.xml",

    ],
    
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
