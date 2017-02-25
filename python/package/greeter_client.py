import grpc
from python.package import helloworld_pb2


def main():
    channel = grpc.insecure_channel('localhost:50051')

    stub = helloworld_pb2.GreeterStub(channel)

    response = stub.SayHello(
        helloworld_pb2.HelloRequest(name='foo')
    )

    print(response)


if __name__ == '__main__':
    main()
