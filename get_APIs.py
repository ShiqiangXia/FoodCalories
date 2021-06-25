from fatsecret import Fatsecret

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

def set_up_api():
    #FatSecret
    consumer_key = 'c9cf8fed3da74f7085018f0d0e89f160'
    consumer_secret = '1c0e39b64cf4456690692d8b3a7312b7'
    try:
        fs = Fatsecret(consumer_key, consumer_secret)
    except:
        print("API Connect Failed")
    # Clarifai
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key 88bd12794cbd4bd99b619c186dbbb32e'),)

    #Logmeal
    #api_user_token = '8f70f86c217f00acf23db4ce097cda0d8c45887d'
    api_user_token = 'db9d236a25ed6ecd43b3db799d3117c66a927500'
    headers = {'Authorization': 'Bearer ' + api_user_token}


    return(fs, stub, metadata, headers)