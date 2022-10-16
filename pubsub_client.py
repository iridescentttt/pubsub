import grpc
import pubsub_pb2
import pubsub_pb2_grpc
import sys


class PubSubClient():
    def __init__(self):
        # 连接 rpc 服务器
        self.channel = grpc.insecure_channel('localhost:2333')
        # 调用 rpc 服务
        self.stub = pubsub_pb2_grpc.PubSubStub(self.channel)

    def SubscribeRequest(self, channelName, delayTime):
        response = self.stub.Subscribe(pubsub_pb2.SubscribeRequest(channelName=channelName,delayTime=delayTime))
        return response
    
    def PublishRequest(self,channelName,msg,delayTime):
        response = self.stub.Publish(pubsub_pb2.PublishRequest(channelName=channelName,msg=msg,delayTime=delayTime))
        return response

    def HelpInfo(self):
        print("usage: ")
        print("python3 pubsub_client.py publish channelchannelName msg delayTime")
        print("python3 pubsub_client.py subscribe channelchannelName delayTime")

def run():
    client=PubSubClient()
    if len(sys.argv) == 5 and sys.argv[1]=="publish" and sys.argv[4].isnumeric():
        if int(sys.argv[4])<0:
            print("delayTime must not be negative")
            exit()
        response=client.PublishRequest(channelName=sys.argv[2],msg=sys.argv[3],delayTime=int(sys.argv[4]))
        print(response)
    elif len(sys.argv) == 4 and sys.argv[1]=="subscribe" and sys.argv[3].isnumeric():
        if int(sys.argv[3])<0:
            print("delayTime must not be negative")
            exit()
        response=client.SubscribeRequest(channelName=sys.argv[2],delayTime=int(sys.argv[3])) 
        for res in response:
            print(res)
    else: 
        client.HelpInfo()

if __name__ == '__main__':
    run()
