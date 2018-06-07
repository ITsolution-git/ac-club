# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Cambodian - Accounting',
    'version': '2.0',
    'description': """
Cambodian Accounting: Chart of Account.
====================================

Cambodian accounting chart and localization.

Odoo allows to manage Cambodian Accounting by providing Two Formats Of Chart of Accounts i.e Cambodian Chart Of Accounts - Standard and Cambodian Chart Of Accounts - Schedule VI.

Note: The Schedule VI has been revised by MCA and is applicable for all Balance Sheet made after
31st March, 2011. The Format has done away with earlier two options of format of Balance
Sheet, now only Vertical format has been permitted Which is Supported By Odoo.
  """,
    'category': 'Localization',
    'depends': [
        'account',
    ],
    'data': [
        'data/l10n_in_chart_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_chart_template_data.yml',
    ],
}
