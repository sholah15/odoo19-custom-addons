QUnit.test("integer rejects letters", async (assert) => {

    input.value = "123abc";

    input.dispatchEvent(
        new Event("input")
    );

    assert.strictEqual(
        input.value,
        "123"
    );
});
