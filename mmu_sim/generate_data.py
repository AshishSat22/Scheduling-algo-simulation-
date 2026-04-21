import random

# Constants
PAGE_SIZE = 256
NUM_PAGES = 256
TOTAL_SIZE = PAGE_SIZE * NUM_PAGES

def generate_binary_store():
    # Create a dummy binary file with recognizable data
    # Each byte is just its page number to make verification easy
    with open("data/backing_store.bin", "wb") as f:
        for i in range(NUM_PAGES):
            page_data = bytes([i] * PAGE_SIZE)
            f.write(page_data)
    print("Generated data/backing_store.bin")

def generate_addresses(count=1000):
    # Generate random 16-bit addresses (range 0 to 65535)
    with open("data/addresses.txt", "w") as f:
        for _ in range(count):
            address = random.randint(0, 65535)
            f.write(f"{address}\n")
    print("Generated data/addresses.txt")

if __name__ == "__main__":
    import os
    if not os.path.exists("data"):
        os.makedirs("data")
    generate_binary_store()
    generate_addresses()
