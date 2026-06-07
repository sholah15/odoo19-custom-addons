/** @odoo-module **/

import { makeView } from "@web/../tests/views/helpers";

QUnit.module("safe_fields", () => {

    QUnit.test("safe_monetary blocks exponent", async function (assert) {

        await makeView({

            type: "form",

            resModel: "safe.fields.tester",

            arch: `
                <form>
                    <field name="price"
                           widget="safe_monetary"
                           options="{'currency_field':'currency_id'}"/>
                </form>
            `,

            serverData: {
                models: {
                    "safe.fields.tester": {
                        fields: {
                            price: {
                                string: "Price",
                                type: "monetary",
                            },
                            currency_id: {
                                string: "Currency",
                                type: "many2one",
                                relation: "res.currency",
                            },
                        },

                        records: [
                            {
                                id: 1,
                                price: 0,
                                currency_id: 1,
                            },
                        ],
                    },

                    "res.currency": {
                        fields: {
                            name: {
                                string: "Name",
                                type: "char",
                            },
                            symbol: {
                                string: "Symbol",
                                type: "char",
                            },
                        },

                        records: [
                            {
                                id: 1,
                                name: "USD",
                                symbol: "$",
                            },
                        ],
                    },
                },
            },
        });

        const input = target.querySelector("input");

        input.value = "1e6";
        input.dispatchEvent(
            new Event("input", { bubbles: true })
        );

        assert.strictEqual(
            input.value,
            "16"
        );
    });

});
