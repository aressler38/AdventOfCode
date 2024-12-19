from multiprocessing import Process, Queue, current_process, freeze_support
from queue import Empty
from aoc2024.emulator import Emulator


def worker(input_queue, program_output):
    i, j = input_queue.get()

    for rax in range(i, j):
        emu = Emulator()
        emu.rax = rax
        emu.run()
        program_output.put((rax, emu.output))


def main():
    NUM_PROCESSES = 2
    rax_per_process = 3
    input_queue = Queue()
    output_queue = Queue()
    rax_offset = 0

    for p in range(NUM_PROCESSES):
        for rax in range(rax_per_process):
            input_queue.put((rax_offset + p, rax_offset + rax * rax_per_process))

    for _ in range(NUM_PROCESSES):
        Process(target=worker, args=(input_queue, output_queue)).start()

    for p in range(NUM_PROCESSES):
        for rax in range(rax_per_process):
            print(output_queue.get(timeout=1))
    rax_offset += NUM_PROCESSES * rax_per_process



if __name__ == "__main__":
    freeze_support()
    main()
