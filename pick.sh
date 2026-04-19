#!/usr/bin/env bash
set -euo pipefail

exercises=()
while IFS= read -r path; do
    # strip leading ./ and trailing /exercise.py
    rel="${path#./}"
    rel="${rel%/exercise.py}"
    exercises+=("$rel")
done < <(find . -path "*/[0-9]*_*/exercise.py" ! -path "*/machine_learning/*" | sort)

n=${#exercises[@]}
count=${1:-1}

if (( count > n )); then
    echo "error: requested $count but only $n exercises available" >&2
    exit 1
fi

# Fisher-Yates shuffle, take first $count
echo
for (( i = 0; i < count; i++ )); do
    j=$(( i + RANDOM % (n - i) ))
    tmp="${exercises[i]}"; exercises[i]="${exercises[j]}"; exercises[j]="$tmp"
    echo "$((i + 1)). ${exercises[i]}"
done
echo
