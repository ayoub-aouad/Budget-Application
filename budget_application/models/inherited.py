from odoo import models, fields, api, _   
from odoo.exceptions import ValidationError
import sys
from datetime import datetime
class MxOop:
    @classmethod
    def create_object(cls, self, comodel_name, field_existe):
        # Vérifier l'existence d'object :
        # - Si oui alors récupéré cet objet
        # - Sinon alors créé un nouveau objet
        res = self.env[comodel_name].search([(''+ field_existe + '.id', '=', self.id)]) 
        action_id = res.id
        if not res:
            return {
                'name': _('Budget'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': comodel_name,
                'domain': [('name', '=', 'None')],
                'view_id': False,
                'type':'ir.actions.act_window',
            }
        else:
            view_id = self.env.ref('budget_application.budget_form_view').id
            return {
                'name': _('Budget'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': comodel_name,
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'res_id': action_id
            } 
class InheritedProject(models.Model):
    _inherit='project.project'
    purchase_request = fields.One2many('purchase.request', 'project_id', string='Purchase Request')
    @api.multi
    def project_budget(self):
        return MxOop.create_object(
            self,
            "budget.budget", 
            'project_id'
        )




class InheritedTask(models.Model):
    _inherit ='project.task'
    purchase_request = fields.One2many('purchase.request', 'task_id', string='Purchase Request')
    @api.multi
    def task_budget(self):
        return MxOop.create_object(
            self,
            "budget.budget", 
            'task_id'
        )

class RequestPurchase(models.Model):
    ''' module qui nous permet de calculer le budget '''
    _inherit = 'purchase.request'

    postes_id = fields.Many2one('budget.post', string = 'Post Ref',)
    project_id = fields.Many2one('project.project', string = 'Project Ref',)
    task_id = fields.Many2one('project.task', string = 'Task Ref',)

    # Constrains :
    @api.constrains('line_ids')
    def _check_all_budget(self):
        """ Constraint pour les budgets """
        calculation = 0
        count = 0
        for rec in self:
            for ref in rec.line_ids:
                for ret in ref.product_id:
                        calculation += ret.lst_price * ref.product_qty
            if rec.postes_id:
                for rep in rec.postes_id:
                    if calculation > rep.budget_theori:
                        raise ValidationError(f"Vous avez dépasser Le budget théorique \nVous avez besoin d'augmenter le budget theorique par {-rep.budget_theori + calculation}DH !!")
    