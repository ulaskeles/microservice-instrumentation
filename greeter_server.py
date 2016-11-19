from concurrent import futures
import sys
import time
import grpc

import helloworld_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2.GreeterServicer):

    def __init__(self, seconds):
        self.seconds = seconds

    def SayHello(self, request, context):
        time.sleep(self.seconds)
        return helloworld_pb2.HelloReply(message='Hello, %s!, time is %s' % (
            request.name, long(time.time())))


def serve(port, seconds):
    seconds = float(seconds)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2.add_GreeterServicer_to_server(Greeter(seconds), server)
    server.add_insecure_port('[::]:%s' % port)
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve(sys.argv[1], sys.argv[2])
