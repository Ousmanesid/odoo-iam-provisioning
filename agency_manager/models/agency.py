from odoo import models, fields, api

class AgencyManager(models.Model):
    _name = 'agency.manager'
    _description = 'Gestion des agences de voyages qui sont des entreprises individuelles d\'accompagnateurs'

    # Informations de base de l'agence
    name = fields.Char(string="Nom de l'agence", required=True)
    siret = fields.Char(string="Numéro SIRET", required=True)
    date_creation = fields.Date(string="Date de création", required=True)
    owner_firstname = fields.Char(string="Prénom du propriétaire", required=True)
    owner_lastname = fields.Char(string="Nom du propriétaire", required=True)
    owner_birthdate = fields.Date(string="Date de naissance du propriétaire", required=True)
    owner_birthplace = fields.Char(string="Lieu de naissance du propriétaire", required=True)
    capital = fields.Float(string="Capital de l'agence", required=True)
    
    # Relations avec les accompagnateurs (partenaires)
    guide_ids = fields.Many2many(
        'res.partner',
        'agency_guide_rel',
        'agency_id',
        'partner_id',
        string="Accompagnateurs",
        domain=[('is_guide', '=', True)],
        help="Liste des accompagnateurs travaillant pour cette agence"
    )
    
    # Relations avec les circuits
    circuit_ids = fields.One2many(
        'agency.circuit',
        'agency_id',
        string="Circuits proposés",
        help="Circuits organisés par cette agence"
    )
    
    # Champs calculés
    guide_count = fields.Integer(
        string="Nombre d'accompagnateurs",
        compute='_compute_guide_count',
        store=True
    )
    
    circuit_count = fields.Integer(
        string="Nombre de circuits",
        compute='_compute_circuit_count',
        store=True
    )

    _sql_constraints = [
        ('unique_siret', 'unique(siret)', 'Le numéro SIRET doit être unique !')
    ]

    @api.depends('guide_ids')
    def _compute_guide_count(self):
        for agency in self:
            agency.guide_count = len(agency.guide_ids)

    @api.depends('circuit_ids')
    def _compute_circuit_count(self):
        for agency in self:
            agency.circuit_count = len(agency.circuit_ids)

    def action_view_guides(self):
        """Action pour afficher les accompagnateurs de l'agence"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accompagnateurs',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.guide_ids.ids)],
            'context': {'default_is_guide': True}
        }

    def action_view_circuits(self):
        """Action pour afficher les circuits de l'agence"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Circuits',
            'res_model': 'agency.circuit',
            'view_mode': 'tree,form',
            'domain': [('agency_id', '=', self.id)],
            'context': {'default_agency_id': self.id}
        }


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Extension du modèle Partner pour les accompagnateurs
    is_guide = fields.Boolean(string="Est un accompagnateur", default=False)
    skills = fields.Text(string="Compétences")
    availability_start = fields.Date(string="Disponible à partir du")
    availability_end = fields.Date(string="Disponible jusqu'au")
    hourly_rate = fields.Float(string="Tarif horaire (€)", digits=(10, 2))
    
    # Relation inverse avec les agences
    agency_ids = fields.Many2many(
        'agency.manager',
        'agency_guide_rel',
        'partner_id',
        'agency_id',
        string="Agences partenaires"
    )


class AgencyCircuit(models.Model):
    _name = 'agency.circuit'
    _description = 'Circuits proposés par les agences'
    
    name = fields.Char(string="Nom du Circuit", required=True)
    circuit_id = fields.Char(string="Identifiant de circuit", required=True)
    start_date = fields.Date(string="Date de début", required=True)
    end_date = fields.Date(string="Date de fin", required=True)
    
    # Relation avec l'agence
    agency_id = fields.Many2one(
        'agency.manager',
        string="Agence",
        required=True,
        ondelete='cascade'
    )
    
    # Informations complémentaires
    description = fields.Text(string="Description du circuit")
    price = fields.Float(string="Prix (€)", digits=(10, 2))
    max_participants = fields.Integer(string="Nombre maximum de participants")
    
    # Accompagnateur assigné
    guide_id = fields.Many2one(
        'res.partner',
        string="Accompagnateur assigné",
        domain=[('is_guide', '=', True)]
    )
    
    _sql_constraints = [
        ('unique_circuit_id', 'unique(circuit_id)', 'L\'identifiant de circuit doit être unique !'),
        ('check_dates', 'check(end_date >= start_date)', 'La date de fin doit être postérieure à la date de début !')
    ] 