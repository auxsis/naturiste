# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class pos_promotion(models.Model):
    _name = "pos.promotion"
    _description = "Management Promotion on pos"

    name = fields.Char('Name', required=1)
    active = fields.Boolean('Active', default=1)
    start_date = fields.Datetime('Start date', default=fields.Datetime.now(), required=1)
    end_date = fields.Datetime('End date', required=1)
    type = fields.Selection([
        ('1_discount_total_order', '1. Discount each amount total order'),
        ('2_discount_category', '2. Discount each category'),
        ('3_discount_by_quantity_of_product', '3. Discount each quantity of product'),
        ('4_pack_discount', '4. Buy pack products discount products'),
        ('5_pack_free_gift', '5. Buy pack products free products'),
        ('6_price_filter_quantity', '6. Sale off products filter by quantity'),
        ('7_special_category', '7. Discount each special category'),
        ('8_discount_lowest_price', '8. Discount lowest price'),
        ('9_multi_buy', '9. Multi buy - By X for price'),
        ('10_buy_x_get_another_free', '10. Buy x (qty) get y (qty) free'),
    ], 'Type', default='1_discount_total_order', required=1, help=
        '1: each total amount of order, each discount\n'
        '2: each category set each discount\n'
        '3: each quantities of product each discount\n'
        '4: set pack products customer buy, discount another products\n'
        '5: set pack products customer buy, free products gift \n'
        '6: each quantity product customer buy, each price\n'
        '7: discount or free gift when customer buy product of category selected \n'
        '8: set discount on product lowest price of list products customer buy\n'
        '9: part of quantity product will apply another price (low of sale price product)\n'
        '10: Buy min x quantity get total qty / min (qty) free')
    product_id = fields.Many2one('product.product', 'Product service', domain=[('available_in_pos', '=', True)])
    discount_order_ids = fields.One2many('pos.promotion.discount.order', 'promotion_id', 'Discounts')
    discount_category_ids = fields.One2many('pos.promotion.discount.category', 'promotion_id', 'Discounts')
    discount_quantity_ids = fields.One2many('pos.promotion.discount.quantity', 'promotion_id', 'Discounts')
    gift_condition_ids = fields.One2many('pos.promotion.gift.condition', 'promotion_id', 'Gifts condition')
    gift_free_ids = fields.One2many('pos.promotion.gift.free', 'promotion_id', 'Gifts apply')
    discount_condition_ids = fields.One2many('pos.promotion.discount.condition', 'promotion_id', 'Discounts condition')
    discount_apply_ids = fields.One2many('pos.promotion.discount.apply', 'promotion_id', 'Discounts apply')
    price_ids = fields.One2many('pos.promotion.price', 'promotion_id', 'Prices')
    special_category_ids = fields.One2many('pos.promotion.special.category', 'promotion_id', 'Special Category')
    discount_lowest_price = fields.Float('Discount lowest price (%)')
    multi_buy_ids = fields.One2many('pos.promotion.multi.buy', 'promotion_id', 'Multi Buy')
    config_ids = fields.Many2many('pos.config',
                                     'pos_config_promotion_rel',
                                     'promotion_id',
                                     'config_id',
                                     string='POS config')
    product_ids = fields.Many2many('product.product', 'promotion_product_rel', 'promotion_id', 'product_id', string='Products group')

    @api.model
    def default_get(self, fields):
        res = super(pos_promotion, self).default_get(fields)
        products = self.env['product.product'].search([('name', '=', 'Promotion service')])
        if products:
            res.update({'product_id': products[0].id})
        return res


class pos_promotion_discount_order(models.Model):
    _name = "pos.promotion.discount.order"
    _order = "minimum_amount"
    _description = "Promotion each total order"

    minimum_amount = fields.Float('Sub total min', required=1)
    discount = fields.Float('Discount %', required=1)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')


class pos_promotion_discount_category(models.Model):
    _name = "pos.promotion.discount.category"
    _order = "category_id, discount"
    _description = "Promotion each product categories"

    category_id = fields.Many2one('pos.category', 'POS Category', required=1)
    discount = fields.Float('Discount %', required=1)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')

    _sql_constraints = [
        ('category_id_uniq', 'unique(category_id)', 'one category only one rule!'),
    ]


class pos_promotion_discount_quantity(models.Model):
    _name = "pos.promotion.discount.quantity"
    _order = "product_id"
    _description = "Promotion discount each product quantities"

    product_id = fields.Many2one('product.product', 'Product', domain=[('available_in_pos', '=', True)], required=1)
    quantity = fields.Float('Minimum quantity', required=1)
    discount = fields.Float('Discount %', required=1)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')


class pos_promotion_gift_condition(models.Model):
    _name = "pos.promotion.gift.condition"
    _order = "product_id, minimum_quantity"
    _description = "Promotion gift condition"

    product_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string='Product',
                                 required=1)
    minimum_quantity = fields.Float('Qty greater or equal', required=1, default=1.0)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1)


class pos_promotion_gift_free(models.Model):
    _name = "pos.promotion.gift.free"
    _order = "product_id"
    _description = "Promotion give gift to customer"

    product_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string='Product gift',
                                 required=1)
    quantity_free = fields.Float('Quantity free', required=1, default=1.0)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')


class pos_promotion_discount_condition(models.Model):
    _name = "pos.promotion.discount.condition"
    _order = "product_id, minimum_quantity"
    _description = "Promotion discount condition"

    product_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string='Product',
                                 required=1)
    minimum_quantity = fields.Float('Qty greater or equal', required=1, default=1.0)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')


class pos_promotion_discount_apply(models.Model):
    _name = "pos.promotion.discount.apply"
    _order = "product_id"
    _description = "Promotion discount apply"

    product_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string='Product',
                                 required=1)
    type = fields.Selection([
        ('one', 'Discount only one quantity'),
        ('all', 'Discount all quantity'),
    ], string='Type', default='one')
    discount = fields.Float('Discount %', required=1, default=1.0)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')


class pos_promotion_price(models.Model):
    _name = "pos.promotion.price"
    _order = "product_id, minimum_quantity"
    _description = "Promotion sale off"

    product_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string='Product',
                                 required=1)
    minimum_quantity = fields.Float('Qty greater or equal', required=1)
    list_price = fields.Float('List Price', required=1)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')


class pos_promotion_special_category(models.Model):
    _name = "pos.promotion.special.category"
    _order = "type"
    _description = "Promotion for special categories"

    category_id = fields.Many2one('pos.category', 'POS Category', required=1)
    type = fields.Selection([
        ('discount', 'Discount'),
        ('free', 'Free gift')
    ], string='Type', required=1, default='discount')
    count = fields.Integer('Count', help='How many product the same category will apply')
    discount = fields.Float('Discount %', required=1)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product apply', domain=[('available_in_pos', '=', True)])
    qty_free = fields.Float('Quantity gift', default=1)


class pos_promotion_multi_buy(models.Model):
    _name = "pos.promotion.multi.buy"
    _description = "Promotion for multi buy"

    product_id = fields.Many2one('product.product', domain=[('available_in_pos', '=', True)], string='Product',
                                 required=1)
    promotion_id = fields.Many2one('pos.promotion', 'Promotion', required=1, ondelete='cascade')
    list_price = fields.Float('Price', required=1)
    next_number = fields.Float('Next number', required=1)

    _sql_constraints = [
        ('product_id_uniq', 'unique(product_id)', 'only one product apply one rule!'),
    ]

    @api.model
    def create(self, vals):
        res = super(pos_promotion_multi_buy, self).create(vals)
        if vals.get('next_number') <= 0 or vals.get('list_price') <= 0:
            raise UserError('Next number and list price could not smaller than 0')
        return res

    def write(self, vals):
        if (vals.get('next_number', None) and vals.get('next_number') <= 0) or (
                vals.get('list_price', None) and vals.get('list_price') <= 0):
            raise UserError('Next number and list price could not smaller than 0')
        return super(pos_promotion_multi_buy, self).write(vals)
