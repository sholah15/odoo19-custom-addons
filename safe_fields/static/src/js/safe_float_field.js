/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FloatField, floatField } from "@web/views/fields/float/float_field";

/**
 * SafeFloatField component
 * 
 * Field input float kustom yang membatasi input pengguna secara real-time
 * untuk mencegah input tidak valid seperti notasi ilmiah (scientific notation)
 * dan karakter non-numerik.
 */
export class SafeFloatField extends FloatField {

    /**
     * Memproses input pengguna secara langsung untuk menyaring karakter yang tidak valid.
     * Hanya memperbolehkan angka, tanda minus (hanya di awal), dan maksimal satu titik/koma desimal.
     * 
     * @param {InputEvent} ev Event input dari browser
     */
    onInput(ev) {
        let value = ev.target.value || "";

        // Blokir scientific notation (e/E)
        value = value.replace(/[eE]/g, "");

        // Sisakan hanya digit, titik, koma, dan minus
        value = value.replace(/[^\d.,\-]/g, "");

        // Tanda minus hanya diperbolehkan di awal karakter
        value = value.replace(/(?!^)-/g, "");

        // Jika terdapat lebih dari satu titik, pertahankan hanya titik pertama
        const dotCount = (value.match(/\./g) || []).length;
        if (dotCount > 1) {
            const parts = value.split(".");
            value = parts[0] + "." + parts.slice(1).join("");
        }

        // Jika terdapat lebih dari satu koma, pertahankan hanya koma pertama
        const commaCount = (value.match(/,/g) || []).length;
        if (commaCount > 1) {
            const parts = value.split(",");
            value = parts[0] + "," + parts.slice(1).join("");
        }

        ev.target.value = value;
    }
}

SafeFloatField.template = "safe_fields.SafeFloatField";

/**
 * Konfigurasi untuk field safe_float
 */
export const safeFloatField = {
    ...floatField,
    component: SafeFloatField,
};

// Daftarkan field safe_float ke registri Odoo
registry.category("fields").add("safe_float", safeFloatField);
