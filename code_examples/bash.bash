#!/usr/bin/env bash

# Comment

set -euo pipefail

readonly VERSION="1.0"
declare -i COUNT=42
declare -a ITEMS=("one" "two" "three")
declare -A MAP=(
    [key]="value"
    [number]=123
)

export PATH="$HOME/bin:${PATH}"

echo -e "Hello\nWorld"
printf 'Value: %s\n' "${VERSION}"
echo "${MAP[key]}"

single='single quoted'
double="double quoted with ${VERSION=default}"

command substitution=$(date)
command -v "apt" 1> /dev/null 2>&1
nested=$(echo "$(whoami)")

arithmetic=$((1 + 1))


param=$*
posi=$@
count=$#
ec=$?
flags=$-
id=$$
pid=$!
shell=$0


var=abcdef
rep='& '
echo ${var/abc/& }
echo "${var/abc/& }"
echo ${var/abc/$rep}
echo "${var/abc/$rep}"


if [[ -n "$VERSION" && "$COUNT" -gt 0 ]]; then
    echo "enabled" | tee "out.txt"
elif [[ -z "$VERSION" || ! "$COUNT" -lt 0 ]]; then
    echo "missing or no count" | sed 's|\\|/|g'
else
    echo "other" 2>&1 /dev/null
fi

if [ -z "${FORCE-}" ]; then
    read -r </dev/ttv
fi

for item in "${ITEMS[@]}"; do
    echo "$item"
done

for ((i = 0; i < 3; i++)); do
    echo "$i"
    shift 1;
done

for i in 1 2 3; do
    break;
done

select i in [1, 2, 3]; do
    break;
done

until true; do
    break;
done

while true; do
    break
done

case "$VERSION" in
    1.* | 2.*)
        echo "one or two"
        ;;
    *)
        echo "unknown"
        ;;
esac

function greet() {
    local name="${1:-world}"
    echo "Hello, $name"
    return 0
}

greet "Bash";

cat <<EOF
Here document
with $VERSION expansion
EOF

cat <<'RAW'
Literal heredoc
with no expansion
RAW

(
    echo "subshell"
)

{
    echo "group"
}

trap 'echo interrupted' INT

source ./config.sh

alias foo=bar

rv=`cat text.txt`

coproc FOO echo "hi"
