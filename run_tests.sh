#!/bin/sh

echo "Running Python tests with unittest..."
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

# Quita los patrones explícitos. Unittest debería descubrirlos por defecto.
python3 -m unittest discover -v tests

# Check the exit status of the unittest command
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed."
    exit 1
fi