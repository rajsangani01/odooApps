# -*- coding: utf-8 -*-
# License LGPL-3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # ------------------------------------------------------------------
    #  USER FIELDS
    # ------------------------------------------------------------------

    restrict_relational_create_user = fields.Boolean(
        string="Disable Create/Edit on All Relational Fields",
        help=(
            "If enabled, this user will NOT be able to create or edit records from relational fields "
            "(Many2one / Many2many).\n"
            "- Hides 'Create' and 'Create and Edit...' in dropdowns.\n"
            "- User can select only existing records.\n"
            "\nAdmins always bypass this restriction."
        ),
    )

    restrict_relational_model_ids = fields.Many2many(
        'ir.model',
        string="Restrict Creation For Specific Models",
        help=(
            "Choose models where this user is NOT allowed to create/edit "
            "records through relational fields.\n"
            "Used only when the global restriction is disabled."
        ),
    )

    # ------------------------------------------------------------------
    #  RPC METHOD FOR FRONTEND (JS)
    # ------------------------------------------------------------------

    @api.model
    def get_relational_restrictions(self, uid):
        """
        Called by JS patch to know:
          - Whether 'Create' should be disabled globally
          - Which models should be restricted individually
        Always executed with sudo() to avoid ir.model ACL errors.
        """
        user = self.sudo().browse(uid)

        # Always return clean list of model technical names
        model_list = user.restrict_relational_model_ids.mapped("model") or []

        return {
            "restrict_relational_create_user": bool(user.restrict_relational_create_user),
            "restrict_relational_model_ids": model_list,
        }

    def action_clear_relational_restrictions(self):
        for user in self:
            user.write({
                'restrict_relational_create_user': False,
                'restrict_relational_model_ids': [(5, 0, 0)],
            })
        return True
