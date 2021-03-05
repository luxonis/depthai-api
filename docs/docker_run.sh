#!/bin/bash

set -e

./docs/update_docs.sh

when-changed -r docs/source -c "bash /app/docs/update_docs.sh" &

python3 -m http.server --bind 0.0.0.0 8000 --directory build/docs/sphinx