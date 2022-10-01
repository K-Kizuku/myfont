release: apt-get update && apt-get upgrade -y
release: pt-get install -y libgl1-mesa-dev
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}