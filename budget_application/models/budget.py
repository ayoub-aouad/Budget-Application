from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import sys
from datetime import datetime

class BudgetModel(models.Model):
    _name = 'budget.budget'
    _description = 'Budget'
    _rec_name = 'name'

    # Front-end
    name = fields.Char(string='Nom', required=False)
    budget_theori = fields.Float(string='Budget Théorique', required=False, digits=(16, 2))
    budget_previ = fields.Float(string='Budget Prévisionnel', required=False, digits=(16, 2), readonly=True, compute='calculate_budget')
    budget_reel = fields.Float(string='Budget Réel', required=False, digits=(16, 2), readonly=True, compute='calculate_budget')

    budget_selection = fields.Selection(string='Répartition', 
                                        selection =[('total', 'Par Totalité'),
                                                    ('tranche', 'Par Tranches')
                                                ], 
                                        required=False)
    
    project_id =fields.Many2one('project.project', string='Project Parent')
    task_id =fields.Many2one('project.task', string='Task Parent')
    
    # Relational Fields   
    post_ids = fields.One2many(
        string="Postes Suivent",
        comodel_name="budget.post",
        inverse_name="budget_id",
        help="Poste Suivent."
    )

    tranches_ids = fields.One2many(
        string="Tranches Suivent",
        comodel_name="budget.distrubition",
        inverse_name="budget_id",
        help="Tranches Suivent."
    )

    # Constrains :
    @api.constrains('tranches_ids','post_ids')
    def _check_all_budget(self):
        """ Constraint pour les budgets """
        calculation = 0
        count = 0
        for rec in self:
            if rec.budget_theori < 0 :
                raise ValidationError("Le budget théorique doit être supérieur ou égal à 0 !!")
            for res in rec.tranches_ids:
                calculation += res.amount
            if calculation > rec.budget_theori:
                raise ValidationError(f"Vous avez dépasser Le budget théorique \nVous avez besoin d'augmenter le budget theorique par {-rec.budget_theori + calculation}DH !!")
            for ref in rec.post_ids:
                count += ref.budget_theori
            if count > rec.budget_theori:
                raise ValidationError(f"Vous avez dépasser Le budget théorique \nVous avez besoin d'augmenter le budget theorique par {-rec.budget_theori + count}DH !!")
    

    @api.depends('post_ids')
    def calculate_budget(self):
        reel = 0
        prev = 0
        for rec in self:
            if rec.post_ids:
                for res in rec.post_ids:
                    prev += res.budget_previ
                    reel += res.budget_reel
            rec.budget_previ = prev 
            rec.budget_reel = reel       