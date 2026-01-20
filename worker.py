import os
from dotenv import load_dotenv  # 🟢 ADD THIS

# 🟢 LOAD .ENV BEFORE DOING ANYTHING ELSE
load_dotenv()

import redis
import time
from rq import SimpleWorker, Queue

# The queue name must match what you use in database.py
listen = ['default']
# 🟢 Use the dynamic URL from .env (for AWS) or fallback to local
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

def run_worker():
    print("👷 Windows Worker Initializing...")
    print(f"🔑 checking key loaded: {'YES' if os.getenv('GEMINI_API_KEY') else 'NO'}") # Debug print
    
    while True:
        try:
            # Setup Connection
            conn = redis.from_url(redis_url)
            conn.ping() # Check if Redis is alive
            
            print("✅ Connected to Redis.")
            
            # Initialize Queue and Worker
            queues = [Queue(name, connection=conn) for name in listen]
            
            # Check for abandoned jobs from previous crashes
            for q in queues:
                count = len(q)
                if count > 0:
                    print(f"📦 Found {count} waiting jobs in '{q.name}' queue.")

            print("📡 Waiting for Video Jobs... (Press Ctrl+C to stop)")
            
            # Start working
            worker = SimpleWorker(queues, connection=conn)
            worker.work()
            break # Exit loop if worker finishes cleanly
            
        except redis.exceptions.ConnectionError:
            print("❌ Redis Server not found. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Worker Error: {str(e)}")
            time.sleep(5)

if __name__ == '__main__':
    run_worker()