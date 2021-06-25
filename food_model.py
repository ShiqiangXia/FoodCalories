
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

        output_text = 'What I see in the picture<br />'

        for ii in range(max_concept):
            output_text +='%d. %s, %.1f%%<br />'%(ii+1, output[ii]['name'], output[ii]['value']*100)
            
        #--------- Predict dish -----------
        predict = IR.food_dish_detetion(headers, file_path)
        pred_food_name = predict['name']
        output_text += '---'*10
        output_text += '<br />Therefore, I predict the dish is<br />'
        output_text += '[ %s ] with prob  %.1f%%<br />'%(pred_food_name, predict['prob']*100)
        

        if predict['subclasses']:
            
            output_text += 'Possible sub dishes: <br />'
            for item in predict['subclasses']:
                if item['prob']>0.1:
                    output_text += '  * %s with prob %.1f%%<br />'%(item['name'], item['prob']*100)
                    
        #--------- Get Nutrition Facts -----------
        pred_food_nutritio = FC.find_food_nutrition(fs, pred_food_name)

        output_text += '---'*10
        output_text += '<br />Here is the nutrition I found for this food: <br />'
       
        output_text += 'Name: %s<br />'%pred_food_nutritio[0].name
        output_text += '1 serving: %.2f g<br />'%pred_food_nutritio[0].serving_amount
        output_text += 'Calorie: %.2f cal <br />Carbs: %.2f g <br />Fat: %.2f g <br />Protein: %.2f g'\
             %(pred_food_nutritio[0].cal, pred_food_nutritio[0].carb, pred_food_nutritio[0].fat, pred_food_nutritio[0].protein)
        return(output_text)
    else :
        
        output_text = 'There seems no food in the image <br />'
        output_text += 'Here are the [concepts] what I see:<br />'
        for ii in range(max_concept):
            output_text += '%d. %s  <br />' %(ii+1, general_out[ii])
            
        return(output_text)
        



