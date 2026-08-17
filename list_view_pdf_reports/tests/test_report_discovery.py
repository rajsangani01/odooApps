# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install', 'list_view_pdf_reports')
class TestListViewPdfReports(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report_model = cls.env['ir.actions.report']
        cls.partner_model = cls.env['res.partner']

        # Create a test partner
        cls.test_partner = cls.partner_model.create({
            'name': 'Test Partner PDF',
            'email': 'test_pdf@example.com',
        })

        # Create a dummy test PDF report bound to res.partner
        cls.test_report = cls.report_model.create({
            'name': 'Test Partner Card PDF',
            'model': 'res.partner',
            'report_name': 'base.report_partner_test',
            'report_type': 'qweb-pdf',
            'show_in_list_view': True,
        })

    def test_get_reports_for_model(self):
        """Test retrieving reports for a model."""
        reports = self.report_model.get_reports_for_model('res.partner')
        report_ids = [r['id'] for r in reports]
        self.assertIn(self.test_report.id, report_ids)

    def test_disabled_report_not_in_list(self):
        """Test that reports with show_in_list_view=False are excluded."""
        self.test_report.show_in_list_view = False
        reports = self.report_model.get_reports_for_model('res.partner')
        report_ids = [r['id'] for r in reports]
        self.assertNotIn(self.test_report.id, report_ids)

    def test_get_valid_reports_for_record(self):
        """Test record specific valid report discovery."""
        reports = self.report_model.get_valid_reports_for_record('res.partner', self.test_partner.id)
        report_ids = [r['id'] for r in reports]
        self.assertIn(self.test_report.id, report_ids)

    def test_invalid_model_returns_empty(self):
        """Test passing an invalid model returns an empty list."""
        reports = self.report_model.get_reports_for_model('non.existing.model')
        self.assertEqual(reports, [])
