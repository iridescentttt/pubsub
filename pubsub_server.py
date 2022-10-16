from concurrent import futures
import time
import grpc
import pubsub_pb2
import pubsub_pb2_grpc

# 实现 proto 文件中定义的 PubSubServer
class PubSubServer(pubsub_pb2_grpc.PubSubServicer):
    def __init__(self):
        self.msgMap = {}

    # 实现 proto 文件中定义的 rpc 调用
    def Subscribe(self, request, context):
        try:
            channelName, delayTime = request.channelName, request.delayTime
            print("New Subscribe Request")
            print(f"Channel Name: {channelName} | Delay time {delayTime}\n")
            time.sleep(delayTime)
            if channelName not in self.msgMap.keys():
                self.msgMap[channelName]=[]
            
            yield pubsub_pb2.Response(msg=f'Subscribe to channel {channelName} successfully!')
            yield pubsub_pb2.Response(msg=f'Channel Message:') 
            for msg in self.msgMap[channelName]:
                yield pubsub_pb2.Response(msg=f'{msg}')
        except: 
                yield pubsub_pb2.Response(msg=f'Subscribe to channel {channelName} failed!')
    
    def Publish(self, request, context):
        try:
            channelName, delayTime,msg = request.channelName, request.delayTime,request.msg
            print("New Publish Request")
            print(f"Channel Name: {channelName} | Delay time {delayTime} | Msg {msg}\n")
            time.sleep(delayTime)
            if channelName in self.msgMap.keys():
                self.msgMap[channelName].append(msg)
            else:
                self.msgMap[channelName]=[msg]
            return pubsub_pb2.Response(msg = f'Publish to channel {channelName} successfully!')
        except:
            return pubsub_pb2.Response(msg=f'Publish to channel {channelName} failed!')

def serve():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pubsub_pb2_grpc.add_PubSubServicer_to_server(PubSubServer(), server)
    server.add_insecure_port('[::]:2333')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
