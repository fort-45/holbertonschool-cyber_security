#!/usr/bin/python3
"""
This module provides a tool to read and write to the heap of a running process.
It searches for a specific string within the heap memory of a given PID
and replaces it with another string.
"""

import sys


def get_heap_info(pid):
    """
    Parses the maps file to find the heap memory range for a given process.
    Checks if the heap is writable.

    Args:
        pid (int): The process ID.

    Returns:
        tuple: (start_address, end_address) as integers.
    """
    maps_path = "/proc/{}/maps".format(pid)
    try:
        with open(maps_path, 'r') as f:
            for line in f:
                if "[heap]" in line:
                    parts = line.split()
                    # Check for 'w' in permissions (parts[1])
                    if 'w' not in parts[1]:
                        return None, None
                    addr = parts[0]
                    start, end = addr.split("-")
                    return int(start, 16), int(end, 16)
    except (FileNotFoundError, PermissionError):
        return None, None
    return None, None


def replace_string(pid, search_str, replace_str):
    """
    Searches for a string in the heap and replaces it with padding.

    Args:
        pid (int): The process ID.
        search_str (str): The string to search for.
        replace_str (str): The string to replace it with.
    """
    start, end = get_heap_info(pid)
    if start is None:
        # Silently fail or exit as per requirement
        sys.exit(1)

    mem_path = "/proc/{}/mem".format(pid)
    try:
        with open(mem_path, "rb+") as f:
            f.seek(start)
            data = f.read(end - start)
            search_bytes = search_str.encode("ascii")
            index = data.find(search_bytes)

            if index == -1:
                sys.exit(1)

            # Pad the replacement string with null bytes if it's shorter
            # to ensure the old string is fully overwritten
            replace_bytes = replace_str.encode("ascii")
            payload = replace_bytes.ljust(len(search_bytes), b'\x00')

            f.seek(start + index)
            f.write(payload)
            print("SUCCESS!")

    except (FileNotFoundError, PermissionError):
        sys.exit(1)


if __name__ == "__main__":
    """
    Main entry point of the script.
    Usage: ./read_write_heap.py pid search_string replace_string
    """
    if len(sys.argv) != 4:
        print("Usage: {} pid search_string replace_string".format(sys.argv[0]))
        sys.exit(1)

    try:
        pid = int(sys.argv[1])
        search_str = sys.argv[2]
        replace_str = sys.argv[3]
        replace_string(pid, search_str, replace_str)
    except ValueError:
        sys.exit(1)
