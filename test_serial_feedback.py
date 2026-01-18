import pty
import os
import select
import sys

def create_virtual_serial():
    # Create a pseudo-terminal pair
    master, slave = pty.openpty()
    slave_name = os.ttyname(slave)
    
    print(f"✓ Virtual serial port created: {slave_name}")
    print(f"Use this in your Python script: SERIAL_PORT = '{slave_name}'")
    print("\nWaiting for data (Ctrl+C to exit)...\n")
    
    try:
        while True:
            # Check if data is available
            if select.select([master], [], [], 0.1)[0]:
                data = os.read(master, 1024)
                msg = data.decode('utf-8', errors='ignore').strip()
                print(f"📥 RECEIVED: {msg}")
                
                # Echo back a response (simulating Arduino)
                response = f"ACK:{msg}\n"
                os.write(master, response.encode('utf-8'))
    
    except KeyboardInterrupt:
        print("\n✓ Virtual port closed")
        os.close(master)
        os.close(slave)

if __name__ == "__main__":
    create_virtual_serial()