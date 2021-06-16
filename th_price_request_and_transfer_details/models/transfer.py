from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    price_list_id = fields.Many2one(
        'product.pricelist',
        string='Liste de price',
        default=1,
        required=True
    )
    total_price_achat_ht = fields.Float(
        string="Total au prix d'achat HT", )
    tota_taxe = fields.Float(string="Total TVA", )
    total_price_achat_ttc = fields.Float(
        string="Total au prix d'acaht TTC", )
    total_price = fields.Float(
        string="Total au prix de vente", )

    
    @api.onchange('move_ids_without_package','move_line_ids_without_package')
    def onchange_field(self):
        for rec in self:
            for l in self.move_ids_without_package:
                l.subtotal_sale_price = l.selling_price * l.product_uom_qty
                l.subtotal_purchase_price = l.x_studio_prix_dachat * l.product_uom_qty
            total_sale = 0
            total_purchase = 0
            for l in self.move_ids_without_package:
                total_sale += l.subtotal_sale_price
                total_purchase += l.subtotal_purchase_price

            purchase_tva = total_purchase * 18/100
            self.total_price = total_sale
            self.total_price_achat_ht = total_purchase
            self.tota_taxe += purchase_tva
            self.total_price_achat_ttc = total_purchase + purchase_tva
    

    @api.onchange('price_list_id')
    def onchange_price_list_id(self):
        for rec in self:
            if not self.price_list_id:
                return
            prices = self.get_price_list(self.price_list_id.item_ids)
            for l in self.move_ids_without_package:
                l.selling_price = l.product_id.lst_price
                for el in prices:
                    if el.product_tmpl_id.id == l.product_id.id:
                        if l.product_qty >= el.min_quantity:
                            if el.compute_price == 'fixed':
                                l.selling_price = el.fixed_price
                            elif el.compute_price == 'percentage':
                                l.selling_price = l.product_id.lst_price - \
                                    (l.product_id.lst_price *
                                     el.percent_price / 100)
                    else:
                        l.selling_price = l.product_id.lst_price
                l.subtotal_sale_price = l.selling_price * l.product_uom_qty
                l.subtotal_purchase_price = l.x_studio_prix_dachat * l.product_uom_qty
            total_sale = 0
            total_purchase = 0
            for l in self.move_ids_without_package:
                total_sale += l.subtotal_sale_price
                total_purchase += l.subtotal_purchase_price

            purchase_tva = total_purchase * 18/100
            self.total_price = total_sale
            self.total_price_achat_ht = total_purchase
            self.tota_taxe += purchase_tva
            self.total_price_achat_ttc = total_purchase + purchase_tva

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


class StockMoveIherit(models.Model):
    _inherit = 'stock.move'

    selling_price = fields.Float(
        string="Prix de vente", )
    subtotal_sale_price = fields.Float(
        string="Sous total du prix de vente", )
    subtotal_purchase_price = fields.Float(
        string="Sous total du prix d'achat", )


class StockMoveLineIherit(models.Model):
    _inherit = 'stock.move.line'

    selling_price = fields.Float(
        string="Prix de vente", )
    subtotal_sale_price = fields.Float(
        string="Sous total du prix de vente", )
    subtotal_purchase_price = fields.Float(
        string="Sous total du prix d'achat", )
