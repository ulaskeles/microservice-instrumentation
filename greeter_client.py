from __future__ import print_function

import sys
import grpc
import time

import helloworld_pb2


def callback(future):
    try:
        print(future.result().message)
    except grpc.RpcError as ge:
        if ge._state.code == grpc.StatusCode.CANCELLED:
            print('Request canceled')
        elif ge._state.code == grpc.StatusCode.UNAVAILABLE:
            print('Service unavailable')
    except Exception as e:
        print(e)


def run():
    channel1 = grpc.insecure_channel('localhost:50051')
    stub1 = helloworld_pb2.GreeterStub(channel1)

    channel2 = grpc.insecure_channel('localhost:50052')
    stub2 = helloworld_pb2.GreeterStub(channel2)

    while True:
        try:
            future1 = stub1.SayHello.future(
                helloworld_pb2.HelloRequest(name='foo'))

            future2 = stub2.SayHello.future(
                helloworld_pb2.HelloRequest(name='bar'))

            future1.add_done_callback(callback)
            future2.add_done_callback(callback)

            time.sleep(5)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    run()
