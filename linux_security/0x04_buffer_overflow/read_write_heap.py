#!/usr/bin/python3
"""
HOLBERTON CYBERSECURITY - PROJECT: BUFFER OVERFLOW
Task 0: Heap Manipulation via /proc filesystem.

This script demonstrates how Linux handles process memory as a file.
By accessing /proc/[PID]/mem, we can bypass standard process
restrictions (if we have root privileges).
"""

import sys


def print_usage():
    """Prints clear instructions for the team."""
    print("Usage: sudo ./read_write_heap.py pid search_string replace_string")
    print("Example: sudo ./read_write_heap.py 1234 'Holberton' 'Hackerton'")


def main():
    """Main entry point for memory manipulation."""
    # 1. ARGUMENT VALIDATION
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    pid = sys.argv[1]
    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    # Convert strings to bytes (Python 3 strings are Unicode)
    search_bytes = search_str.encode('ascii')
    replace_bytes = replace_str.encode('ascii')

    # 2. SECURITY CHECK: BUFFER INTEGRITY
    if len(replace_bytes) > len(search_bytes):
        print(f"[!] Warning: Replace string is longer than search string.")
        print("    This will likely cause a Segfault in the target process.")

    # 3. PARSING /proc/[PID]/maps
    try:
        with open(f"/proc/{pid}/maps", "r", encoding="utf-8") as maps_file:
            heap_info = None
            for line in maps_file:
                if "[heap]" in line:
                    parts = line.split()
                    addr_range = parts[0].split('-')
                    heap_start = int(addr_range[0], 16)
                    heap_end = int(addr_range[1], 16)

                    if 'w' not in parts[1]:
                        print(f"[!] Error: Heap at {parts[0]} not writable.")
                        sys.exit(1)

                    heap_info = (heap_start, heap_end, parts[0])
                    break

            if not heap_info:
                print(f"[!] Error: Could not locate [heap] for PID {pid}")
                sys.exit(1)

        heap_start, heap_end, addr_str = heap_info

        # 4. ACCESSING /proc/[PID]/mem
        with open(f"/proc/{pid}/mem", "r+b") as mem_file:
            mem_file.seek(heap_start)
            heap_data = mem_file.read(heap_end - heap_start)

            # 5. SEARCH AND REPLACE
            offset = heap_data.find(search_bytes)
            if offset == -1:
                print(f"[!] Error: '{search_str}' not found in the heap.")
                sys.exit(1)

            actual_addr = heap_start + offset

            # Pad with Null Bytes if the replacement is shorter
            payload = replace_bytes.ljust(len(search_bytes), b'\x00')

            mem_file.seek(actual_addr)
            mem_file.write(payload)

    except PermissionError:
        print("[!] Access Denied: You MUST run this script with 'sudo'.")
    except FileNotFoundError:
        print(f"[!] Error: Process {pid} does not exist.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
