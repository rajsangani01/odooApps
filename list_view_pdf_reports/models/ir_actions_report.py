# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    show_in_list_view = fields.Boolean(
        string="Show in List View",
        default=True,
        help="If enabled, this PDF report will appear in the List View row PDF dropdown menu."
    )

    @api.model
    def get_reports_for_model(self, model_name):
        """Retrieve all active PDF reports associated with the model accessible by the current user.
        
        :param str model_name: Technical name of the Odoo model (e.g. 'sale.order')
        :return: list of dicts with report metadata
        """
        if not model_name or model_name not in self.env:
            return []

        # Check model read access for current user
        if not self.env['ir.model.access'].check(model_name, mode='read', raise_exception=False):
            return []

        # Search reports bound to model or having model equal to model_name
        reports = self.search([
            '|', ('model', '=', model_name), ('binding_model_id.model', '=', model_name),
            ('report_type', 'in', ['qweb-pdf', 'qweb-text']),
            ('show_in_list_view', '=', True)
        ])

        user = self.env.user
        result = []
        for report in reports:
            # Group restriction check
            if report.group_ids and not (report.group_ids & user.all_group_ids):
                continue

            result.append({
                'id': report.id,
                'name': report.name,
                'report_name': report.report_name,
                'report_type': report.report_type,
                'domain': report.domain or False,
            })

        return result

    @api.model
    def get_valid_reports_for_record(self, model_name, record_id):
        """Return valid reports for a single record, checking domain criteria and record security rules.
        
        :param str model_name: Technical model name
        :param int record_id: Database ID of the record
        :return: list of dicts of valid reports for the record
        """
        reports = self.get_reports_for_model(model_name)
        if not reports or not record_id:
            return reports

        record = self.env[model_name].browse(record_id)
        if not record.exists():
            return []

        # Enforce record security rules
        try:
            record.check_access('read')
        except Exception:
            return []

        valid_reports = []
        for rep in reports:
            rep_domain = rep.get('domain')
            if rep_domain:
                try:
                    eval_domain = safe_eval(rep_domain)
                    if not record.filtered_domain(eval_domain):
                        continue
                except Exception as e:
                    _logger.warning("Error evaluating domain for report %s on record %s: %s", rep.get('id'), record_id, e)
            valid_reports.append(rep)

        return valid_reports
