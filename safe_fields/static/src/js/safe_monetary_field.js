/** @odoo-module **/

import { registry } from "@web/core/registry";
import { MonetaryField, monetaryField } from "@web/views/fields/monetary/monetary_field";

export class SafeMonetaryField extends MonetaryField {

    onInput(ev) {
        let value = ev.target.value || "";

        // Hapus scientific notation
        value = value.replace(/[eE]/g, "");

        // Sisakan digit, titik, koma, dan minus
        value = value.replace(/[^\d.,\-]/g, "");

        // Minus hanya boleh di awal
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

        super.onInput(ev);
    }
}

export const safeMonetaryField = {
    ...monetaryField,
    component: SafeMonetaryField,
};

registry.category("fields").add(
    "safe_monetary",
    safeMonetaryField
);
