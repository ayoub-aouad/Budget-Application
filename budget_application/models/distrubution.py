from odoo import models, fields, api, _   

class DistrubutionBudget(models.Model):
    _name = 'budget.distrubition'

    name = fields.Char(string='Nom', required=False)
    amount = fields.Float(string='Montant Desponible', required=False, digits=(16, 2))
    date_previ = fields.Datetime(string='Date Prévisionnel', required=True)
    date_reel = fields.Datetime(string='Date Réel', required=True)
    
    budget_id = fields.Many2one('budget.budget', string='Parent Budget')