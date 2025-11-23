/** @odoo-module **/

import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";

patch(Many2XAutocomplete.prototype, {
    setup() {
        super.setup(...arguments);

        this.user_restrictions = null;
        this.is_admin_user = false;

        // cache to avoid repeating calculations (per widget instance)
        this._is_blocked_cache = null;

        // kick off loads but do not await (non-blocking UI)
        this._loadUserRestrictions();
        this._loadAdminGroup();
    },

    // ------------------------------------------------------------
    //  LOAD USER RESTRICTIONS FROM PYTHON RPC (safe)
    // ------------------------------------------------------------
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
            // normalize model ids to array of strings
            if (!Array.isArray(this.user_restrictions.restrict_relational_model_ids)) {
                this.user_restrictions.restrict_relational_model_ids = [];
            }
        } catch (e) {
            // don't break the widget — log for debugging and keep defaults
            console.error("Failed to load relational restrictions:", e);
            this.user_restrictions = { restrict_relational_create_user: false, restrict_relational_model_ids: [] };
        } finally {
            // reset cache so next check will use loaded values
            this._is_blocked_cache = null;
        }
    },

    // ------------------------------------------------------------
    //  CHECK ADMIN GROUP (safe)
    // ------------------------------------------------------------
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

    // ------------------------------------------------------------
    //  RESTRICTION LOGIC (GLOBAL + MODEL-WISE) with caching
    // ------------------------------------------------------------
    _isCreateBlocked() {
        // return cached value if computed
        if (this._is_blocked_cache !== null) {
            return this._is_blocked_cache;
        }

        // if not loaded, do not block by default (avoid UI break)
        if (!this.user_restrictions) {
            this._is_blocked_cache = false;
            return false;
        }

        // admin bypass
        if (this.is_admin_user) {
            this._is_blocked_cache = false;
            return false;
        }

        const restrictAll = !!this.user_restrictions.restrict_relational_create_user;
        const restrictedModels = this.user_restrictions.restrict_relational_model_ids || [];

        // get model name safely
        const targetModel = typeof this.props?.resModel === "string" ? this.props.resModel : undefined;

        // global block
        if (restrictAll) {
            this._is_blocked_cache = true;
            return true;
        }

        // model-wise block (only if targetModel exists)
        if (targetModel && Array.isArray(restrictedModels) && restrictedModels.includes(targetModel)) {
            this._is_blocked_cache = true;
            return true;
        }

        // allow by default
        this._is_blocked_cache = false;
        return false;
    },

    // ------------------------------------------------------------
    //  OVERRIDES (complete replacements — do not call super)
    // ------------------------------------------------------------
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