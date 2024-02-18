python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
export OPENAI_API_KEY=""
cd webui
reflex init
reflex run