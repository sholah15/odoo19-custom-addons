/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FloatField } from "@web/views/fields/float/float_field";

export class SafeFloatField extends FloatField {

    onInput(ev) {
        let value = ev.target.value || "";

        value = value.replace(/[eE]/g, "");
        value = value.replace(/[^\d.\-]/g, "");

        const parts = value.split(".");
        if (parts.length > 2) {
            value = parts[0] + "." + parts.slice(1).join("");
        }

        value = value.replace(/(?!^)-/g, "");

        ev.target.value = value;

        super.onInput(ev);
    }
}

registry.category("fields").add("safe_float", SafeFloatField);
