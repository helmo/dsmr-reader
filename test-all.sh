#!/bin/bash

echo ""
echo "--- Running Pylama for code audit..."
pylama

# Abort when audit fails.
if [ $? -ne 0 ]; then
    echo "[!] Code audit failed"
    exit;
fi

echo "OK"

echo ""
echo "--- Testing with SQLite (4 processes)..."
pytest --pylama --cov --cov-report=html:coverage_report/html --cov-report=term --ds=dsmrreader.config.test.sqlite -n 4


echo ""
echo "--- Testing with PostgreSQL (4 processes)..."
pytest --pylama --cov --cov-report=html:coverage_report/html --cov-report=term --ds=dsmrreader.config.test.postgresql -n 4


echo ""
echo "--- Testing with MySQL (1 process due to concurrency limitations)..."
pytest --pylama --cov --cov-report=html:coverage_report/html --cov-report=term --ds=dsmrreader.config.test.mysql


# Remove annoying headers that get regenerated every time.
sed -i '/"PO-Revision-Date:/d' dsmrreader/locales/nl/LC_MESSAGES/django.po
sed -i '/"POT-Creation-Date:/d' dsmrreader/locales/nl/LC_MESSAGES/django.po

sed -i '/"PO-Revision-Date:/d' docs/locale/nl/LC_MESSAGES/*.po
sed -i '/"POT-Creation-Date:/d' docs/locale/nl/LC_MESSAGES/*.po
