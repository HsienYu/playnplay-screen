import pytchat
import time
chat = pytchat.create(video_id="jfKfPfyJRdk")
while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}", flush=True)
