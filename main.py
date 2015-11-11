# Multi-level Feedback Queue Scheduling for tasks

import Queue from queue

queues = [ Queue(i*10, i) for i in range(256)]
# pendingProcs: [(pid, QIndex)]
pendingProcs = []
currProc = None
# At each timer tick (timer interval iterrupt triggered
# and this is the kernel-level handler)
def schedule():
    global currProc
    # is true except for the very first process to be scheduled at boot up
    if currProc is not None:
        # index and queue of residence of currently executing process
        index = currProc.priority

        Q = queues[index]

        p = currProc
        # if p is blocking for I/O
        if p.blocking == 1:
            # save process state to PCB
            # TODO
            Q.dequeue()

            # if p is at the top level
            if index == 0:
                Q.enqueue(p)

            # if p is not at the top level
            else:
                queues[index-1].enqueue(p)

        # if p leaves voluntarily
        elif p.leave == 1:
            # save process state to PCB
            # TODO
            Q.dequeue()

            pendingProcs.append({"pid" : p.PID, "Qindex" : index})

        # in all other cases, the process is marked as running
        # one cycle in the CPU
        else:
            # 1 unit in queue's quantum time for task has been used up
            p.Qtime =-1
            # 1 unit of task's time has been completed
            p.time -=1
            # if the task has used up available quantum time
            if p.Qtime <= 0:
                # save process state to PCB
                # TODO

                # remove from current queue
                Q.dequeue()
                # and is not yet completed
                if p.time > 0:
                    # add to next lowest queue
                    queues[index + 1].enqueue(p)
                # and is completed
                else:
                    # TODO: destroy p
                    pass

            # if quantum time is not complete but task is completed
            elif p.time <= 0:
                Q.dequeue()
                # TODO: destroy p

            #nothing to be done. Else clause only included for completeness
            else:
                pass

    # goes through each of the 256 queues
    for Q in enumerate(queues):
        # empty queues are disregarded
        if not Q.isEmpty():
            # assign CPU to first process in first nonempty queue
            p = Q.peek()
            currProc = p
            # send p to CPU
            break

def addToQueue(process):
    # if the process previously yielded and is now returning to the queue
    if (entry = filter(lambda pp: pp["pid"] == process, pendingProcs)) is not None:
        # place back in the queue it yielded from
        queues[entry["Qindex"]].enqueue(process)
    else:
        # place in the top queue
        queues[0].enqueue(process)
