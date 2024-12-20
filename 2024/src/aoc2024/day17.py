import itertools
import queue
import time
from multiprocessing import Process, Queue, current_process, freeze_support
from queue import Empty
from aoc2024.emulator import Emulator


def consumer(input_queue, program_output):
    try:
        emu = Emulator()
        emu.load_rom()
        while True:
            emu.reset()
            rax = input_queue.get(timeout=5)
            emu.rax = rax
            emu.run()
            # print("emu output", emu.output)
            program_output.put((rax, emu.output))
    except Empty:
        print("Finished")


def producer(input_queue, bit_length, max_input_queue_size):
    try:
        for bits in itertools.product([0, 1], repeat=bit_length - 1):
            in_qsize = input_queue.qsize()
            if max_input_queue_size < in_qsize:
                # print('hit max in')
                time.sleep(0.8)
                continue
            rax = 1 << bit_length
            for shift, bit in enumerate(bits):
                rax += bit << shift
            input_queue.put(rax)
    except queue.Full:
        print("QUEUE IS FULL")
    print("Finished")


def found_solution(output_queue, input_queue, target_output, stats):
    try:
        output = output_queue.get_nowait()
    except Empty:
        return False
    rax, program_output = output
    stats['counter'] += 1
    if stats['counter'] % 1000000 == 0:
        out_qsize = output_queue.qsize()
        in_qsize = input_queue.qsize()
        print(time.time(), "counter =", stats['counter'], "output_queue_size = ", out_qsize, "input_queue_size = ", in_qsize, "stats: ",
              stats)
    if program_output == target_output:
        print("success at rax = ", rax)
        with open('../../data/day17-output.txt', 'w') as f:
            f.write(str(rax))
            f.write("\n")
            f.write(str(program_output))
            f.write("\n")
        return True
    return False


def main():
    target_output = [2, 4, 1, 7, 7, 5, 1, 7, 0, 3, 4, 1, 5, 5, 3, 0]
    num_processes = 24  # I have a 16 core AMD 5950X. Technically 32 threads, but we'll see.
    rax_per_process = 300
    input_queue = Queue()
    output_queue = Queue()
    bit_length = 45
    processes = []
    max_input_queue_size = 1e5
    stats = {'counter': 0}

    print(time.time(), "queue size:", input_queue.qsize())

    for _ in range(num_processes):
        p = Process(target=consumer, args=(input_queue, output_queue))
        processes.append(p)
        p.start()

    p = Process(target=producer, args=(input_queue, bit_length, max_input_queue_size))
    processes.append(p)
    p.start()

    while True:
        if found_solution(output_queue, input_queue, target_output, stats):
            break

    print("finished main")
    for p in processes:
        p.kill()
        p.join()
        p.close()


if __name__ == "__main__":
    freeze_support()
    main()
    print("Exit")
