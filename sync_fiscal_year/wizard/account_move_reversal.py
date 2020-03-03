# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api, _


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'
    _description = 'Account Move Reversal'

    def _get_period(self):
        ctx = dict(self._context)
        period_ids = []
        check_period_ids = self.env['account.period'].search([])
        if check_period_ids:
            period_ids = self.env['account.period'].with_context(ctx).find()
        return period_ids and period_ids[0] or False

    period_id = fields.Many2one('account.period', 'Period', required=True, default=lambda self: self._get_period())

    @api.onchange('date')
    def _onchange_date(self):
        period_id = False
        if self.date:
            period_id = self.env['account.period'].search([('state', '!=', 'done'), ('date_start', '<=', self.date), ('date_stop', '>=', self.date), ('company_id', '=', self.env.user.company_id.id)], limit=1)
        if period_id:
            self.period_id = period_id.id
