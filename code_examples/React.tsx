/// <reference types="react" />

import type { ReactNode } from "react";
import { useState } from "react";

type Props<T = string> = {
    title: string;
    value?: T;
    children?: ReactNode;
    enabled: boolean;
};

interface Item {
    id: number;
    name: string;
}

const items: Item[] = [
    { id: 1, name: "One" },
    { id: 2, name: "Two" },
];

function Card<T extends object>({
    title,
    value,
    children,
    enabled,
}: Props<T>) {
    const [count, setCount] = useState<number>(0);

    const className = enabled
        ? "active"
        : "disabled";

    return (
        <>
            {/* JSX comment */}

            <section
                id="card"
                className={className}
                data-count={count}
                hidden={!enabled}
            >
                <h1>{title}</h1>

                <p>
                    Value: {String(value ?? "none")}
                </p>

                <button
                    type="button"
                    onClick={() => setCount(count + 1)}
                >
                    Click {count}
                </button>

                {items.map((item) => (
                    <ItemRow
                        key={item.id}
                        name={item.name}
                    />
                ))}

                {enabled && (
                    <span>
                        {children}
                    </span>
                )}
            </section>
        </>
    );
}

const element = (
    <Card<number>
        title="Example"
        value={42}
        enabled
    >
        <strong>Child</strong>
    </Card>
);

export default Card;
