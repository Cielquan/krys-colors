/// <reference types="node" />

import type { ReadonlyArray as List } from "types";
import { readFile } from "fs";

export const VERSION: string = "1.0";

type ID = string | number;
type Nullable<T> = T | null;
type Handler = (value: ID) => Promise<void>;

interface Extendable {
    foo?: string;
}

interface User<T = unknown> extends Extendable {
    readonly id: ID;
    name: string;
    data?: T;
}

class Account implements User<string> {
    public readonly id: ID;
    private secret: string;
    protected active = true;

    constructor(id: ID, secret: string) {
        this.id = id;
        this.secret = secret;
    }

    get name(): string {
        return "account";
    }

    set name(value: string) {
        console.log(value as string);
    }
}

enum Status {
    Idle,
    Running = "running",
}

const x = Status.Idle;

namespace Utils {
    export function log(message: string): void {
        console.log(message);
    }
}

@sealed
class Service {
    async fetch<T extends object>(value: T): Promise<T> {
        await Promise.resolve();
        return value as T;
    }

}

function process(
    input: Nullable<ID>,
    callback?: Handler,
): List<string> {
    const tuple: [string, number] = ["value", 42];

    const obj = {
        ...tuple,
        ["key"]: true,
    };

    if (input ?? false) {
        callback?.(input);
    }

    switch (input) {
        case null:
            break;
        case undefined:
            break;
        default:
            return [`${input}`];
    }

    return [];
}

const arrow = <T>(value: T): T => value;

const regex = /test\d+/gi;

const raw = String.raw`line\n${VERSION}`;

export default process;
