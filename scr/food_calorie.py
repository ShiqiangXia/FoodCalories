
#Food 
# FatSecret API
from fatsecret import Fatsecret

class MyFood:
    
    def __init__(self, name, food_id,serving_amount, cal, carb, fat, protein):
        self.name = name
        self.food_id = food_id
        self.serving_amount = serving_amount
        self.cal = cal
        self.carb = carb
        self.fat = fat
        self.protein = protein
        self.normalized_flag = False
        
    def show_nutrition_facts(self):
        print('---'*10)
        print('Food name: %s' % self.name)
        print('Food id: %s' % self.food_id)
        print('1 serving: %.2f g'  % self.serving_amount)
        print('Calorie: %.2f cal, Carbs: %.2f g, Fat: %.2f g, Protein: %.2f g' %(self.cal, self.carb, self.fat, self.protein))

    def normalize_serving(self):
        if self.serving_amount:
            goal = 100.0;
            current = self.serving_amount;
            if current!= goal:
                self.serving_amount = goal;
                ratio = goal/current ;
                self.cal *= ratio;
                self.carb *= ratio;
                self.fat  *= ratio;
                self.protein *= ratio;
            self.normalized_flag = True;
           
        else:
            print('This food "%s" has not serving amount info, we can not normalize it.' % self.name)
            
            
    def calculate_nutrition(self, amount_g):
        if self.serving_amount:
            ratio = amount_g/self.serving_amount
        else:
            print('Warning: This food has not serving amount info')
            ratio = 1.0; 
        return [self.cal*ratio, self.carb*ratio, self.fat * ratio, self.protein * ratio]    

def find_food_nutrition(response, name, max_results = 3):

    try:
        foods = response.foods_search(name, max_results = max_results)
    except:
        print("Food %s is not found!"%name)
    else:
        id_list = [f['food_id'] for f in foods]
        if len(id_list)>=max_results:
            id_list = id_list[0:max_results]
    
    food_list = [];
    
    for idx in id_list:
        food = response.food_get(idx)
        all_servings = food['servings']['serving']
        if isinstance(all_servings,list):
            chosen_serving = all_servings[0]
        else:
            chosen_serving = all_servings
        try : 
            serving_amount = chosen_serving['metric_serving_amount']
            serving_amount = float(serving_amount)
        except:
            serving_amount = None
            
        name =  food['food_name']   
        cal = float(chosen_serving['calories'])
        carb = float(chosen_serving['carbohydrate'])
        fat = float(chosen_serving['fat'])
        protein = float(chosen_serving['protein'])
             
        temp_food = MyFood(name, idx, serving_amount, cal, carb, fat, protein)
        
        food_list.append(temp_food)
    
    return food_list
        
def meal_nutrition(food_list, amount_list, print_flag = True, break_down = False):
    total = [0.0]*4
    if break_down:
        nutri_list = [];
        
    for ii, food in enumerate(food_list):
        nutrition = food.calculate_nutrition(amount_list[ii])
        for jj in range(4):
            total[jj] += nutrition[jj]
        if break_down:
            nutri_list.append(nutrition)
    
    print('Meal nutrition facts:')
    print('Calorie: %.2f, Carb: %.2f, Fat: %.2f, Protein: %.2f'%(total[0],total[1],total[2],total[3]))
    if break_down:
        print("\nNutrition breakdown:")
        for ii, food in enumerate(food_list):
            print('----'*10)
            temp_nutrition = nutri_list[ii]
            print('%s, amount %s g' %(food.name, amount_list[ii]))
            print('Calorie: %.2f (%.1f%%), Carb: %.2f (%.1f%%), Fat: %.2f (%.1f%%), Protein: %.2f (%.1f%%)'%
                  (temp_nutrition[0],100*temp_nutrition[0]/total[0],
                   temp_nutrition[1],100*temp_nutrition[1]/total[1],
                   temp_nutrition[2],100*temp_nutrition[2]/total[2],
                   temp_nutrition[3],100*temp_nutrition[3]/total[3]))
            
def meal__nutrition_calculator(response, name_list, amount_list):
    food_list = [];
    for foo in name_list:
        temp_food = find_food_nutrition(fs,foo)[0]
        food_list.append(temp_food)
        temp_food.normalize_serving()
        #temp_food.show_nutrition_facts()
    meal_nutrition(food_list,amount_list,break_down=True)            
        
            
                
                
        
        

        