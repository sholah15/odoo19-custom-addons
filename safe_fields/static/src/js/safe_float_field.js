/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FloatField, floatField } from "@web/views/fields/float/float_field";
import { parseFloat } from "@web/views/fields/parsers";

export class SafeFloatField extends FloatField {

    onInput(ev) {
        let value = ev.target.value || "";

        // blok scientific notation
        value = value.replace(/[eE]/g, "");

        // sisakan digit, titik, koma dan minus
        value = value.replace(/[^\d.,\-]/g, "");

        // minus hanya boleh di depan
        value = value.replace(/(?!^)-/g, "");

        // Jika user mengetik lebih dari satu titik
        const dotCount = (value.match(/\./g) || []).length;
        if (dotCount > 1) {
            const parts = value.split(".");
            value = parts[0] + "." + parts.slice(1).join("");
        }

        // Jika user mengetik lebih dari satu koma
        const commaCount = (value.match(/,/g) || []).length;
        if (commaCount > 1) {
            const parts = value.split(",");
            value = parts[0] + "," + parts.slice(1).join("");
        }

        ev.target.value = value;
    }
}

export const safeFloatField = {
    ...floatField,
    component: SafeFloatField,
};

registry.category("fields").add(
    "safe_float",
    safeFloatField
);
