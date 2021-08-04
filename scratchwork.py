# use of the Timer
import time

def main():
    start = time.perf_counter()
    stop = time.perf_counter()

    elapsedTime = stop - start


# Timeout variables initialized
sampleRTT = # some number
estimatedRTT = sampleRTT
devRTT = 0
alpha = .875
beta = .75

# Update with each new sample RTT
estimatedRTT = alpha * estimatedRTT + (1 - alpha) * sampleRTT
devRTT = beta * devRTT + (1 - beta) * abs(sampleRTT - estimatedRTT)
timeout = estimatedRTT + 4 * devRTT


# rough layout of the Program
nextSeqNum = initialSeqNum
sendBase = initialSeqNum
timerRunning = False # Boolean to keep track of timer

while #still more to send

    #if there is data to be sent
    if len(data) > 0:
        #create TCP segment using nextSeqNum
        if not timerRunning:
            start = time.perf_counter()
        # pass segment to IP
        nextSeqNum = nextSeqNum + length(data)

    # case where the time elapsed has passed the timeout limit
    current = time.perf_counter()
    if  (current - start) >= timout:
        #retransmit segment with smallest seqNum
        start = time.perf_counter()
        timerRunning = True

    # ACK received (y)
    if y > sendBase:
        sendBase = y
        if # no ACKed segments:
            start = time.perf_counter()
            timerRunning = True
