# goldpump-rain-notifier

wrote this because running a headless chrome instance 24/7 just to grab goldpump rain events was eating too much ram. 

this connects straight to their socket.io gateway with wsbypass, listens for rain-stream, and fires off a discord embed whenever a pot starts or finishes.

requirements:
pip install -r requirements.txt

how to run:
drop your webhook link into HOOK in main.py
python main.py
