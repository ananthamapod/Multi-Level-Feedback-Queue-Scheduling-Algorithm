# Multilevel Feedback Queue Scheduling Algorithm

The multilevel feedback queue is a method of kernel scheduling that attempts to resolve the problems associated with First-Come-First-Serve (FCFS) scheduling and Shortest-Job-First (SJF) scheduling, namely inefficient turnaround times for interactive and real-time processes and job starvation respectively.

Multilevel feedback queue (MLFQ) scheduling uses a system of queues, each designated a different priority. Each queue is assigned a different quantum time for Round-Robin (RR) scheduling. The important thing to note about MLFQ scheduling is that it is preemptive: a currently running process can be removed from the CPU if another process is deemed to be of higher priority. At each cycle of the CPU, processes can be moved between queues, and therefore the priority of a process can be considered dynamic.

This implementation in Python is a simple demonstration of Multilevel Feedback Queue Scheduling, and is by no means a directly translatable implementation to an operating system's kernel. There are 256 different priorities, and therefore 256 queues in this sample system.

## Transitions to consider
1. New process: goes to first priority queue Q0

2. Process leaves voluntarily (process yields or blocks for I/O): process leaves system and is inserted back in the same queue when it returns

3. Process takes up quantum time at Q[X]: bump down to the next priority queue Q[X+1]

4. Process blocks for I/O at Q[X]: bump up to a higher priority queue Q[X-1] to allow escape from lowest priority level (prevents starving)

## Procedure:
  1. Move processes to their positions

  2. pick first process in topmost queue

*** Given current process currProc and list of queues queues: ***

### First step:
    Q = queue of currProc
    index = index of Q
    p = currProc

    if p is blocking for I/O:
        save processing state to p.PCB

        Q.dequeue()

        if index == 0:
            Q.enqueue(p)

        else:
            queues[index-1].enqueue(p)

        endif

    elif p leaves voluntarily:
        save processing state to p.PCB

        Q.dequeue()

        store (p.pid, index)

    else:
        p.taskTime -= 1

        p.Qtime -= 1

        if quantum time finished (p.Qtime <= 0):
            save processing state to p.PCB
            Q.dequeue()

            if task not finished (p.taskTime > 0):
                queues[index+1].enqueue(p)

            else:
                destroy(p)

            endif

        elif task finished (p.taskTime <= 0):
            Q.dequeue()

            destroy(p)

        else:
            pass

        endif

    endif

### Second step:

    for Q in queues:
      if Q is not empty:
        p = Q.peek()
        currProc = p
        send p to CPU
        break
      endif
    endfor
