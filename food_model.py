
import food_calorie as FC # food nutrition data 
import image_model as IR # analyze image and recognize food

from get_APIs import * 

import requests


from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

def food_model(file_path, max_concept=5):

    fs, stub, metadata, headers = set_up_api()

    #--------- Analyze concepts -----------
    general_out = IR.General_Image_Analysis2(file_path,stub,metadata)

    if 'food' in general_out:

        output = IR.Food_Image_Analysis(file_path,stub,metadata)

        print('What I see in the picture ')
        for ii in range(max_concept):
            print('%d. %s, %.1f%%'%(ii+1, output[ii]['name'], output[ii]['value']*100))

        #--------- Predict dish -----------
        predict = IR.food_dish_detetion(headers, file_path)
        pred_food_name = predict['name']
        print('---'*10)
        print('Therefore, I predict the dish is')
        print('[ %s ] with prob  %.1f%%'%(pred_food_name, predict['prob']*100))

        if predict['subclasses']:
            print('Possible sub dishes: ')
            for item in predict['subclasses']:
                if item['prob']>0.1:
                    print('  * %s with prob %.1f%%'%(item['name'], item['prob']*100))

        #--------- Get Nutrition Facts -----------
        pred_food_nutritio = FC.find_food_nutrition(fs, pred_food_name)

        print('---'*10)
        print('Here is the nutrition I found for this food: ')

        pred_food_nutritio[0].show_nutrition_facts()

        #return(pred_food_name, pred_food_nutritio)
        return('Food %s'%pred_food_name)
    else :
        print('There seems no food in the image')
        print('Here are the [concepts] what I see:')
        for ii in range(max_concept):
            print('%d. %s  ' %(ii+1, general_out[ii]))
        return('no food')
        



