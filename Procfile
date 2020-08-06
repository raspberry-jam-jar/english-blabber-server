web: env PYTHONPATH="$PYTHONPATH:$(pwd)/modules:$(pwd)/conf" daphne asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: env PYTHONPATH="$PYTHONPATH:$(pwd)/modules:$(pwd)/conf" python manage.py runworker -v2
