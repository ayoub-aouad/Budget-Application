from odoo import models , api, fields, _
from odoo.exceptions import ValidationError
import sys
from datetime import datetime

class PostBudgetaire(models.Model):
    _name = 'budget.post'

    name = fields.Char(string='Nom', required=True)
    budget_theori = fields.Float(string='Budget Théorique', required=False, digits=(16, 2),readonly=True,  compute='get_budget_theori')
    budget_porcentage = fields.Float(string='Pourcentage', required=False)
    budget_previ = fields.Float(string='Budget Prévisionnel', required=False, digits=(16, 2), readonly=True,  compute='calculate_budget')
    budget_reel = fields.Float(string='Budget Réel', required=False, digits=(16, 2), readonly=True,  compute='calculate_budget')

    budget_id = fields.Many2one('budget.budget', string='Parent Budget')

    purchase_request = fields.One2many('purchase.request', 'postes_id', string='purchase.request')

    
    @api.depends('budget_porcentage')
    def get_budget_theori(self):
        for rec in self:
            if rec.budget_id:
                for res in rec.budget_id:
                    if res.budget_selection == 'total':
                        rec.budget_theori = rec.budget_porcentage * res.budget_theori / 100
                    else :
                        if res.tranches_ids:
                            for ref in res.tranches_ids:
                                rec.budget_theori = rec.budget_porcentage * ref.amount / 100

    @api.depends('purchase_request')
    def calculate_budget(self):
        count = 0
        for rec in self:
            if rec.purchase_request:
                for res in rec.purchase_request:
                    if res.line_ids:
                        for ref in res.line_ids:
                            for ret in ref.product_id:
                                count = ret.lst_price * ref.product_qty
                                if res.state == 'done':
                                    rec.budget_previ = count
                                    rec.budget_reel = count
                                else:
                                    rec.budget_previ = count

    # Constrains :
    @api.constrains('purchase_request')
    def _check_all_budget(self):
        """ Constraint pour les budgets """
        calculation = 0
        count = 0
        for rec in self:
            if rec.budget_theori < 0 :
                raise ValidationError("Le budget théorique doit être supérieur ou égal à 0 !!")
            for res in rec.purchase_request:
                for ref in res.line_ids:
                    for ret in ref.product_id:
                            calculation += ret.lst_price * ref.product_qty
            if rec.budget_id:
                for rep in rec.budget_id:
                    if calculation > rep.budget_theori:
                        raise ValidationError(f"Vous avez dépasser Le budget théorique \nVous avez besoin d'augmenter le budget theorique par {-rec.budget_theori + calculation}DH !!")
            
    
    
    