#!/usr/bin/python3
"""
This module provides a tool to read and write to the heap of a running process.
It searches for a specific string within the heap memory of a given PID
and replaces it with another string.
"""

import sys
import os


def get_heap_info(pid):
    """
    Parses the maps file to find the heap memory range for a given process.

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
                    addr = line.split()[0]
                    start, end = addr.split("-")
                    return int(start, 16), int(end, 16)
    except (FileNotFoundError, PermissionError):
        print("Error: Could not access /proc/{}/maps".format(pid))
        sys.exit(1)
    return None, None


def replace_string(pid, search_str, replace_str):
    """
    Searches for a string in the heap and replaces it.

    Args:
        pid (int): The process ID.
        search_str (str): The string to search for.
        replace_str (str): The string to replace it with.
    """
    start, end = get_heap_info(pid)
    if start is None:
        print("Error: Could not find [heap] in /proc/{}/maps".format(pid))
        sys.exit(1)

    mem_path = "/proc/{}/mem".format(pid)
    try:
        with open(mem_path, "rb+") as f:
            f.seek(start)
            data = f.read(end - start)
            search_bytes = search_str.encode("ascii")
            index = data.find(search_bytes)

            if index == -1:
                print("Error: String '{}' not found in heap".format(search_str))
                sys.exit(1)

            # Move to the position of the string found
            f.seek(start + index)
            f.write(replace_str.encode("ascii"))
            print("SUCCESS!")

    except (FileNotFoundError, PermissionError):
        print("Error: Could not access /proc/{}/mem".format(pid))
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
        print("Error: PID must be an integer")
        sys.exit(1)
