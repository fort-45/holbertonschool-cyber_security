#!/usr/bin/python3
"""
Module to find and replace a string in the heap of a running process
using the /proc filesystem.
"""
import sys


def find_heap(pid):
    """Read /proc/pid/maps and return heap start and end addresses."""
    heap_start = None
    heap_end = None

    try:
        with open(f"/proc/{pid}/maps", "r", encoding="utf-8") as f:
            for line in f:
                if '[heap]' in line:
                    parts = line.split()
                    addrs = parts[0].split('-')
                    heap_start = int(addrs[0], 16)
                    heap_end = int(addrs[1], 16)
                    break
    except FileNotFoundError:
        print(f"[!] Error: Process {pid} does not exist.")
        sys.exit(1)
    except PermissionError:
        print("[!] Access Denied: Run with sudo.")
        sys.exit(1)

    return heap_start, heap_end


def replace_in_heap(pid, heap_start, heap_end, search, replace):
    """Find search bytes in heap and replace with replace bytes."""
    try:
        with open(f"/proc/{pid}/mem", "r+b") as f:
            f.seek(heap_start)
            heap_data = f.read(heap_end - heap_start)

            offset = heap_data.find(search)
            if offset == -1:
                print("String not found in heap")
                sys.exit(1)

            payload = replace.ljust(len(search), b'\x00')
            f.seek(heap_start + offset)
            f.write(payload)
    except PermissionError:
        print("[!] Access Denied: Run with sudo.")
        sys.exit(1)


def main():
    """Entry point. Parse arguments and manipulate heap."""
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv[1]
    search = sys.argv[2].encode('ascii')
    replace = sys.argv[3].encode('ascii')

    heap_start, heap_end = find_heap(pid)

    if heap_start is None:
        print("Heap not found")
        sys.exit(1)

    replace_in_heap(pid, heap_start, heap_end, search, replace)
    print("SUCCESS!")


if __name__ == "__main__":
    main()
