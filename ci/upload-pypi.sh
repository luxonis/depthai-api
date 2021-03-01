#!/bin/bash

python3 -m pip install -U pip
python3 -m pip install -U setuptools
python3 -m pip install -U twine

# Uploads prebuilt binary distribution
for file in wheelhouse/audited/*.whl; do
    echo "Uploading $file"
    python3 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" "$file"
done

# Uploads zip source distribution
for file in wheelhouse/audited/*.zip; do
    echo "Uploading $file"
    python3 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" "$file"
done

# Uploads tar.gz source distribution
for file in wheelhouse/audited/*.tar.gz; do
    echo "Uploading $file"
    python3 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" "$file"
done