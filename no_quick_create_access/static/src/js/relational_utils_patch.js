/** @odoo-module **/

import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";

patch(Many2XAutocomplete.prototype, {

    setup() {
        super.setup(...arguments);
        this.user_restrictions = null;
        this.is_admin_user = false;
        this._is_blocked_cache = null;
        this._loadUserRestrictions();
        this._loadAdminGroup();
    },

    async _loadUserRestrictions() {
        const userId = user.userId;
        try {
            const data = await this.orm.call(
                "res.users",
                "get_relational_restrictions",
                [userId],
                {}
            );
            this.user_restrictions = data || {};
            console.log('>>>>>>>>>>>>>>>', this.user_restrictions);

            if (!Array.isArray(this.user_restrictions.restrict_relational_model_ids)) {
                this.user_restrictions.restrict_relational_model_ids = [];
            }
        } catch (e) {
            console.error("Failed to load relational restrictions:", e);
            this.user_restrictions = { restrict_relational_create_user: false, restrict_relational_model_ids: [] };
        } finally {
            this._is_blocked_cache = null;
        }
    },

    async _loadAdminGroup() {
        try {
            this.is_admin_user = await user.hasGroup("base.group_system");
        } catch (e) {
            console.error("Failed to check admin group:", e);
            this.is_admin_user = false;
        } finally {
            this._is_blocked_cache = null;
        }
    },

    _isCreateBlocked() {
        if (this._is_blocked_cache !== null) {
            return this._is_blocked_cache;
        }
        if (!this.user_restrictions) {
            this._is_blocked_cache = false;
            return false;
        }

        if (this.is_admin_user) {
            this._is_blocked_cache = false;
            return false;
        }
        const restrictAll = !!this.user_restrictions.restrict_relational_create_user;
        const restrictedModels = this.user_restrictions.restrict_relational_model_ids || [];
        const targetModel = typeof this.props?.resModel === "string" ? this.props.resModel : undefined;
        if (restrictAll) {
            this._is_blocked_cache = true;
            return true;
        }

        if (targetModel && Array.isArray(restrictedModels) && restrictedModels.includes(targetModel)) {
            this._is_blocked_cache = true;
            return true;
        }
        this._is_blocked_cache = false;
        return false;
    },

    addCreateSuggestion({ request }) {
        if (this._isCreateBlocked()) return false;
        return !!this.props.quickCreate && request.length > 0;
    },

    addCreateEditSuggestion({ records, request }) {
        if (this._isCreateBlocked()) return false;
        return (
            (this.activeActions.createEdit ?? this.activeActions.create) &&
            (request.length > 0 || records?.length === 0)
        );
    },
});