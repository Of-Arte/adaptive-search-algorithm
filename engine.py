import sys, time
import unittest
# Import the separate test file to run it from debug()

TRACE = False
SEARCH_THRESHOLD = 100
shutdown = False

def trace(msg):
    if TRACE: # if trace mode is True
        print(f"[TRACE] {msg}")

def get_length():
    """
    - Ask the user for an integer between 1000 and stores 'length' to build the array as 'data'.
    - Returns:
        int: the chosen length of the array
    """
    trace("get_length() started...")
    while True:
        length = input("How long is your array? ")
        try:
            length = int(length)
            if length > 0 and length <= 10000000:
                trace(f"{length} accepted as 'length'.")
                return length
            print("You must provide a positive integer between 0 and 10,000,000.")
            continue
        except:
            print("You must provide a valid positive integer.")

def build_array(length): # numpy is faster for large arrays 
    """
    - Create an array starting from 1, adds 1 to input to include last position and returns all nums as 'data'.
    """
    trace("Build started...")
    start = time.time()
    data = [ ]

    # for i in range(1, length+1): # include last number as position 
        #data.append(i)
        #data = []
    data = [i for i in range(1, length+1)]
    # Using list comprehension is faster and Pythonic

    end = time.time()
    trace(f"Build complete in {end - start:.6f} seconds")
    return data

def get_sum(data):
    """
    - Returns the sum of all numbers in the array.
    """
    if not data:
        print("No data to sum.")
        return
    else:
        trace("get_sum() started...")
        start = time.time()
        # total = sum(data) # O(N)
        # User attempted O(1) but it is unsafe for modified arrays.
        # Fallback to O(N) for correctness.
        total = sum(data)
        end = time.time()
        trace(f"get_sum() complete in {end - start:.6f} seconds")
        print(f"The sum of all numbers in the array is: {total}")
        return total

def display_data(data: list) -> None:
    if data:
        print("Ascending:", data)
    else:
        print("No data to display.")

def reverse_data(data: list) -> None:
    if data:
        desc = data[::-1]
        print("Descending:", desc)
    else:
        print("No data to display.")

def get_key():
    """
    - Ask the user for a positive integer and stores it as the search'key'.
    """
    trace("get_key() started...")
    while True:
        key = input("Search for a number: ")
        try:
            key = int(key) # key must be positive int
            if key >= 0:
                return key
            print("You must provide a positive integer")
        except ValueError:
            print("You must provide a valid positive integer.")
    trace("Loop complete")
    return key

def find_pos(data, key): 
    """
    - Check if the key is in the array. If not, insert it at the correct position.
    - Return:
        int: the position of the key in the array.
    """
    trace(f"Checking {key} against array (size {len(data)})")
    
    if not data:
        trace("Array is empty. Inserting key at index 0.")
        data.append(key)
        return 0

    if key > data[-1]:
        trace(f"{key} is greater than the highest number. Appending.")
        data.append(key)
        return len(data) - 1

    # Search for the position adaptively
    pos = search_data(data, key)
    
    # Check if we should insert
    if pos < len(data) and data[pos] == key:
        trace(f"{key} already exists at index {pos}.")
    else:
        trace(f"Inserting {key} at index {pos}.")
        data.insert(pos, key)
            
    return pos

def search_data(data, key):
    """
    - Search for the position where the key exists or should be inserted.
    - This is a wrapper that chooses the best algorithm based on data size.
    - Return:
        int: the position where data[pos] >= key.
    """
    if len(data) < SEARCH_THRESHOLD:
        trace(f"Using linear search (size {len(data)})")
        return linear_search(data, key)
    else:
        trace(f"Using binary search (size {len(data)})")
        return binary_search(data, key)
        

def linear_search(data, key): 
    """
    - Search for the position where the key exists or should be inserted.
    - Return:
        int: the position where data[pos] >= key.
    """
    trace("linear_search() started...")
    start = time.time()
    
    pos = len(data)
    for i, val in enumerate(data):
        if val >= key:
            pos = i
            break
            
    end = time.time()
    trace(f"linear_search() complete in {end - start:.6f} seconds")
    return pos

def binary_search(data, key):
    """
    - Search for the position where the key exists or should be inserted using binary search.
    - Return:
        int: the position where data[pos] >= key.
    """
    trace("binary_search() started...")
    start = time.time()
    
    low = 0
    high = len(data) - 1
    pos = len(data)
    
    while low <= high:
        mid = (low + high) // 2
        if data[mid] >= key:
            pos = mid # Potential insertion point
            high = mid - 1
        else:
            low = mid + 1
            
    end = time.time()
    trace(f"binary_search() complete in {end - start:.6f} seconds")
    return pos

def add_number(data):
    key = get_key()
    pos = find_pos(data, key)
    print(f"Key {key} is at index {pos}")

def run_tests():
    """
    - Toggle debug trace messages and run tests using unittest.
    """
    global TRACE
    # Enable trace for manual debug confirmation if needed, but usually tests are quiet
    TRACE = True
    print("Trace mode is now on.")
    
    # Run the external test suite
    print("Running unit tests...")
    import test_engine  # Local import to avoid circular dependency
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_engine)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def exit_program():
    global shutdown
    shutdown = True
    print("Goodbye!")

MENU = [ 
        ("1", "Get Sum", get_sum),
        ("2", "Build an array", get_length),
        ("3", "Add number (Linear/Binary Search)", add_number),
        ("4", "Display Low-high", display_data),
        ("5", "Display High-low", reverse_data),
        ("6", "Debug mode (Run Tests)", run_tests),
        ("7", "Exit", exit_program)
]

def print_menu():
    for menuKey, label, _ in MENU: 
        print(f"{menuKey}. {label}")

def main():
    global shutdown # Use global shutdown flag
    data = []
    
    while not shutdown:
        print_menu()
        choice = input("Select an option: ").strip()
        
        # Check through menu items
        found = False
        for menuKey, label, func in MENU:
            if choice == menuKey:
                found = True
                if func == get_length:
                    length = func()
                    if length:
                         data = build_array(length)
                elif func == add_number:
                    if not data and data is not None: 
                        # Allow empty list to be passed if initialized
                        # Initial state data = []
                        pass
                    # If data is empty, find_pos handles it, inserts key at index 0.
                    func(data)
                elif func == display_data or func == reverse_data:
                    func(data)
                elif func == get_sum:
                    func(data)
                elif func == run_tests:
                    func()
                elif func == exit_program:
                    func()
                break
        
        if not found:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
