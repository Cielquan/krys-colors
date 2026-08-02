#!/usr/bin/env node

"use strict";

/* Block comment */
// One line comment

import defaultExport, { named as alias } from "./module.js";

export const VERSION = "1.0";
export default function main() {
    return VERSION;
}

const integer = 42;
const hex = 0xff;
const binary = 0b1010;
const octal = 0o755;
const float = 3.14;
const exponent = 1.2e5;

const enabled = true;
const empty = null;
const missing = undefined;

const symbol = Symbol("id");
const big = 123n;

const regex = /hello\d+/gi;

const template = `Hello ${enabled ? "yes" : "no"}`;

const array = [1, "two", null];
const object = {
    key: "value",
    ["computed"]: 42,
    ...array,
};

const {
    key: renamed = "default",
    ...rest
} = object;

class User extends Object {
    #privateField = 0;

    constructor(name) {
        super();
        this.name = name;
    }

    get value() {
        return this.#privateField;
    }

    async update(value = 0) {
        await Promise.resolve(value);
        return this?.name ?? "unknown";
    }

    *generator() {
        yield 1;
        yield* [2, 3];
    }
}

function process(...args) {
    return args
        .filter(x => x != null)
        .map(x => x ** 2);
}

async function run() {
    try {
        await process(...array);
    } catch (error) {
        throw new Error("failed");
    } finally {
        console.log("done");
    }
}

for (const item of array) {
    if (item === null) {
        continue;
    }
}

for (let i = 0; i < 3; i++) {
    console.log(i);
}

switch (VERSION) {
    case "1.0":
        break;
    default:
        break;
}
