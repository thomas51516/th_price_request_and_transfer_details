from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    price_list_id = fields.Many2one(
        'product.pricelist',
        string='Liste de price',
        default=1,
        required=True
    )
    total_price = fields.Float(string="Total au prix de vente")

    @api.onchange('order_line')
    def onchange_order_line(self):
        for rec in self:
            total = 0
            for l in self.order_line:
                l.subtotal_sale_price = l.selling_price * l.product_uom_qty
                total += l.subtotal_sale_price
        rec.total_price = total

    # @api.onchange('price_list_id')
    def onchange_price_list_id(self):
        if not self.price_list_id:
            return
        prices = self.get_price_list(self.price_list_id.item_ids)
        total = 0
        for l in self.order_line:
            l.selling_price = l.product_id.lst_price
            for el in prices:
                if el.product_tmpl_id.id == l.product_id.id:
                    if l.product_qty >= el.min_quantity:
                        if el.compute_price == 'fixed':
                            l.selling_price = el.fixed_price
                        elif el.compute_price == 'percentage':
                            l.selling_price = l.product_id.lst_price - \
                                (l.product_id.lst_price * el.percent_price / 100)
                else:
                    l.selling_price = l.product_id.lst_price
            l.subtotal_sale_price = l.selling_price * l.product_uom_qty
            total += l.subtotal_sale_price
        self.total_price = total

    def get_price_list(self, liste):
        indexs = []
        for l in liste:
            indexs.append(l.min_quantity)

        indexs.sort()
        # indexs.reverse()
        liste_defi = []

        for a in indexs:
            for p in liste:
                if p.min_quantity == a:
                    liste_defi.append(p)

        return liste_defi


class PurchaseOrderLineIherit(models.Model):

    _inherit = 'purchase.order.line'

    selling_price = fields.Float(string="Prix de vente")
    subtotal_sale_price = fields.Float(string="Sous total du prix de vente")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.price_unit = self.product_qty = 0.0

        self._product_id_change()

        self._suggest_quantity()
        self._onchange_quantity()

        self.product_qty = 1
        self.name = self.product_id.display_name
        self.taxes_id = self.product_id.taxes_id
        self.selling_price = self.product_id.list_price
        self.subtotal_sale_price = self.product_id.list_price * self.product_qty
