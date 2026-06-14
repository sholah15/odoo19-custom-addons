/** @odoo-module **/

import { registry } from "@web/core/registry";
import { IntegerField, integerField } from "@web/views/fields/integer/integer_field";

/**
 * SafeIntegerField component
 * 
 * Field input integer kustom yang membatasi input pengguna secara real-time
 * hanya untuk angka bulat (integer) positif maupun negatif.
 */
export class SafeIntegerField extends IntegerField {

    /**
     * Memproses input pengguna secara langsung untuk menyaring karakter yang tidak valid.
     * Hanya memperbolehkan digit angka dan tanda minus di awal.
     * 
     * @param {InputEvent} ev Event input dari browser
     */
    onInput(ev) {
        let value = ev.target.value || "";

        // Hapus semua karakter kecuali digit angka dan tanda minus
        value = value.replace(/[^\d\-]/g, "");

        // Tanda minus hanya diperbolehkan di awal karakter
        value = value.replace(/(?!^)-/g, "");

        ev.target.value = value;
    }
}

SafeIntegerField.template = "safe_fields.SafeIntegerField";

/**
 * Konfigurasi untuk field safe_integer
 */
export const safeIntegerField = {
    ...integerField,
    component: SafeIntegerField,
};

// Daftarkan field safe_integer ke registri Odoo
registry.category("fields").add("safe_integer", safeIntegerField);
