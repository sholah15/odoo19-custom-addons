/** @odoo-module **/

import { registry } from "@web/core/registry";
import { IntegerField, integerField } from "@web/views/fields/integer/integer_field";

export class SafeIntegerField extends IntegerField {

    onInput(ev) {

        let value = ev.target.value || "";

        // Remove all non-digits and minus
        value = value.replace(/[^\d\-]/g, "");

        // Only one minus at start
        value = value.replace(/(?!^)-/g, "");

        ev.target.value = value;
    }
}

export const safeIntegerField = {
    ...integerField,
    component: SafeIntegerField,
};

registry.category("fields").add(
    "safe_integer",
    safeIntegerField
);
