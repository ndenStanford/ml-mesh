#!/bin/sh

cd "${HOME}" || exit

python -m src.register_trained_model
