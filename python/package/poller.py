import grpc
from tornado import gen
from tornado.ioloop import PeriodicCallback, IOLoop
from python.package import helloworld_pb2


class Poller():

    @gen.coroutine
    def poll(self):
        wait_i = gen.WaitIterator(*self.hello_futures())

        while not wait_i.done():
            try:
                reply = yield wait_i.next()

            except Exception as e:
                print(e)

            else:
                print(reply)

    def hello_futures(self):
        hello_futures = []
        for _ in range(3):
            channel = grpc.insecure_channel('localhost:50051')

            stub = helloworld_pb2.GreeterStub(channel)

            hello_future = stub.SayHello.future(
                helloworld_pb2.HelloRequest(name='foo'),
                timeout = 5
            )
            hello_futures.append(hello_future)

        return hello_futures


def main():
    poller = Poller()
    PeriodicCallback(poller.poll, 10 * 1000).start()
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
