import time
import os

def main():
    try:
        stage = os.environ.get("STAGE", "default")
        print(f"Container is running in STAGE: {stage}")
        print("Listening for events... (press CTRL+C to exit)")
        while True:
            # Replace this with any custom logic or simply keep it alive
            time.sleep(10)
    except KeyboardInterrupt:
        print("Listener stopped. Exiting gracefully.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
