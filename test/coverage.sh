#!/usr/bin/env bash
COVERAGE_FILE=.coverage_params coverage run test_params.py
COVERAGE_FILE=.coverage_pron coverage run test_pronunciation.py
coverage combine .coverage_*
coverage report
