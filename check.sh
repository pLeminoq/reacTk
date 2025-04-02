#!/bin/bash

echo "Black:" &&
black --check reacTk example tests &&
echo "" &&
echo "Flake8:" &&
flake8 --max-line-length 127 reacTk example &&
echo "" &&
echo "PyTest:" &&
pytest tests

