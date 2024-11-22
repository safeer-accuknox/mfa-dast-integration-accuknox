import pyotp
import os
import sched
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(script_dir, 'mfa')

secret = "KZLECXTACUUFMQKZ"
totp = pyotp.TOTP(secret)

scheduler = sched.scheduler(time.time, time.sleep)

def generate_and_save_totp():
    result = totp.now()
    print(f"TOTP Code: {result}")

    with open(output_file_path, 'w') as file:
        file.write(f"{result}")

    scheduler.enter(28, 1, generate_and_save_totp)

scheduler.enter(0, 1, generate_and_save_totp)

scheduler.run()
