import os
import redis
import time
from rq import SimpleWorker, Queue

# The queue name must match what you use in database.py
listen = ['default']
redis_url = 'redis://localhost:6379'

def run_worker():
    print("👷 Windows Worker Initializing...")
    
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