/** @odoo-module **/

import { makeView } from "@web/../tests/views/helpers";

QUnit.module("safe_fields", () => {

    QUnit.test("safe_float blocks letters and exponent", async function (assert) {

        await makeView({
            type: "form",

            resModel: "safe.fields.tester",

            arch: `
                <form>
                    <field name="distance"
                           widget="safe_float"/>
                </form>
            `,

            serverData: {
                models: {
                    "safe.fields.tester": {
                        fields: {
                            distance: {
                                string: "Distance",
                                type: "float",
                            },
                        },
                        records: [
                            { id: 1, distance: 0 },
                        ],
                    },
                },
            },
        });

        const input = target.querySelector("input");

        input.value = "12e3abc";
        input.dispatchEvent(
            new Event("input", { bubbles: true })
        );

        assert.strictEqual(
            input.value,
            "123"
        );
    });

});
