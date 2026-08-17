import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, useState } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.pdfReportsState = useState({
            reportsByModel: {},
            activeRecordId: null,
        });

        onWillStart(async () => {
            await this.loadPdfReports();
        });
    },

    /**
     * Load available PDF reports for the current model once per view load.
     */
    async loadPdfReports() {
        const resModel = this.props.list && this.props.list.resModel;
        if (!resModel || this.pdfReportsState.reportsByModel[resModel]) {
            return;
        }
        try {
            const reports = await this.orm.call(
                "ir.actions.report",
                "get_reports_for_model",
                [resModel]
            );
            this.pdfReportsState.reportsByModel[resModel] = reports || [];
        } catch (error) {
            console.error("[ListViewPdfReports] Error fetching PDF reports for model", resModel, error);
            this.pdfReportsState.reportsByModel[resModel] = [];
        }
    },

    /**
     * Get available reports for a given record.
     * @param {Object} record
     * @returns {Array} List of report dicts
     */
    getRecordPdfReports(record) {
        const resModel = (record && record.resModel) || (this.props.list && this.props.list.resModel);
        if (!resModel) {
            return [];
        }
        return this.pdfReportsState.reportsByModel[resModel] || [];
    },

    /**
     * Mouse enter handler for PDF dropdown container
     * @param {string|number} recordId
     */
    onPdfDropdownMouseEnter(recordId) {
        this.pdfReportsState.activeRecordId = recordId;
    },

    /**
     * Mouse leave handler for PDF dropdown container
     */
    onPdfDropdownMouseLeave() {
        this.pdfReportsState.activeRecordId = null;
    },

    /**
     * Toggle dropdown open state on click
     * @param {string|number} recordId
     */
    togglePdfDropdown(recordId) {
        if (this.pdfReportsState.activeRecordId === recordId) {
            this.pdfReportsState.activeRecordId = null;
        } else {
            this.pdfReportsState.activeRecordId = recordId;
        }
    },

    /**
     * Trigger PDF report generation for a single record row.
     * @param {Object} report
     * @param {Object} record
     */
    async onSelectPdfReport(report, record) {
        // Close dropdown menu on selection
        this.pdfReportsState.activeRecordId = null;

        if (!report || !record || !record.resId) {
            return;
        }
        const context = {
            active_id: record.resId,
            active_ids: [record.resId],
            active_model: record.resModel || (this.props.list && this.props.list.resModel),
        };
        await this.actionService.doAction(report.id, {
            additionalContext: context,
        });
    },
});
