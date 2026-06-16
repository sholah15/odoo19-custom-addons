{
    'name': "Opentelemetry Signoz",
    'version': '19.0.0.1',
    'summary': "Send Opentelemetry Instrumentation of Odoo to Signoz",
    'description': """
        Send Opentelemetry Instrumentation of Odoo to Signoz.

        Trace Output:

        /web/login

        /web/webclient/load_menus

        /web/dataset/call_kw

        sale.order.search

        stock.move.write

        account.move.create

        cron.ir_cron

        cron.stock_scheduler

        PostgreSQL query
    """,
    'author': "Maizar",
    'website': "https://maizarrahman.blogspot.com",
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [],
    'installable': True,
    'auto_install': False,
    "post_load": "post_load",
}
