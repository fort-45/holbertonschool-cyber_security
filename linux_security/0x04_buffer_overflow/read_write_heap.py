#!/usr/bin/python3
"""
Module to find and replace a string in the heap of a running process.
"""
import sys


def find_heap(pid):
    """Read /proc/pid/maps and return heap start and end addresses."""
    maps_file = "/proc/{}/maps".format(pid)
    heap_start = None
    heap_end = None

    with open(maps_file, 'r') as f:
        for line in f:
            if '[heap]' in line:
                parts = line.split()
                addrs = parts[0].split('-')
                heap_start = int(addrs[0], 16)
                heap_end = int(addrs[1], 16)
                break

    return heap_start, heap_end


def replace_in_heap(pid, heap_start, heap_end, search, replace):
    """Find search string in heap and replace it with replace string."""
    mem_file = "/proc/{}/mem".format(pid)

    with open(mem_file, 'rb+') as f:
        f.seek(heap_start)
        heap_data = f.read(heap_end - heap_start)

        offset = heap_data.find(search)
        if offset == -1:
            print("String not found in heap")
            sys.exit(1)

        print("Found '{}' at offset {}".format(search, offset))
        f.seek(heap_start + offset)
        f.write(replace)
        print("Replaced with '{}'".format(replace))


def main():
    """Entry point. Parse arguments and call heap functions."""
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

    print("Heap: 0x{:x} - 0x{:x}".format(heap_start, heap_end))
    replace_in_heap(pid, heap_start, heap_end, search, replace)


if __name__ == "__main__":
    main()

