import openai
import pandas as pd
import pathlib as Path
import os
import ast,sys

from gpt import GPT,Example
 


class GPTHandler:
    def __init__(self) -> None:
        self._filepath_ = os.path.abspath(__file__)
        # Get the directory of the current file
        self._root_dir_ = os.path.dirname(self._filepath_)     
        
        self.suggestions_df = pd.read_excel(os.path.join(self._root_dir_, 'suggestions.xls'),sheet_name='few_short')
        self.api_key = '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'
        self.model_engine='gpt-3.5-turbo-instruct'
        self.temperature =0.05
        self.max_tokens = 100
    
    def load_gpt_model(self,):
        #config settings
        openai.api_key = self.api_key
        unique_inputs =set()

        #load training data
        df = self.suggestions_df

        #Model config
        model_engine = self.model_engine
        temperature = self.temperature
        max_tokens = self.max_tokens

        gpt = GPT(engine = model_engine,temperature=temperature,max_tokens=max_tokens)


        for _,row in df.iterrows():
            input_text = row['input']
            response_text = row['output']


            #check if the input is present in the df
            if input_text in unique_inputs:
                continue

            #example object
            examples = Example(input_text,response_text)
            gpt.add_example(examples)

            unique_inputs.add(input_text)

        return gpt
    
    def get_gpt_response(self,gpt_model,input_text):
        instrunction = """ 
        Given an input question,respond with syntactically correct Python dictionary code.Be creative but the python code should be correct. Only use Python dictionary having keys :['country','country_noc','year']
        """
        prompt = input_text + instrunction
        response = gpt_model.get_top_reply(prompt)
        return response
    
    def preprocess_response(self,response):
        response = response.split("output: ")[-1].strip('\n')
        response = ast.literal_eval(response)
        return response
    
    def apply_filter(self,keys,response,df):
        try:
            filtered_df = df.copy()
            print(filtered_df.head())
            print(response)
            

            for key in keys:
                if key in response:
                    print('---------------------------')
                    print("key : ",key)
                    value = response[key]
                    print('value : ',value)
                    

                    if isinstance(value,list):
                        
                        try:
                            #filtered_df = filtered_df[filtered_df[key].str.lower.isin(list(map(str.lower,value)))]
                            filtered_df = filtered_df[filtered_df[key].str.lower().isin(list(map(str.lower,value)))]     
                            
                            
                        except :
                            filtered_df = filtered_df[filtered_df[key].isin(value)]

                    else:
                        #filtered_df = filtered_df[filtered_df[key].str.lower()==value.lower()]
                        filtered_df = filtered_df[filtered_df[key] == (value)]
                
                
            return filtered_df
        except KeyError as e:
            print(str(e))

