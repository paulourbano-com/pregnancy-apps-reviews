import pandas as pd
import json
import glob
import copy

# Testing github.dev

def add_data(input_dictionary, data):
  temp = copy.copy(input_dictionary)
#   print(input_dictionary, data)
  temp['language_code'] = data
  return(temp)


def get_dictionary_list(input_string, file_name):
  
  result = []
  
  lang_code = ''
  if 'pt_BR' in file_name:
    lang_code = 'pt_BR'
  elif 'en_GB' in file_name:
    lang_code = 'en_GB'
  elif 'pt' in file_name:
    lang_code = 'pt'
  elif 'es' in file_name:
    lang_code = 'es'
  elif 'fr' in file_name:
    lang_code = 'fr'
  elif 'de' in file_name:
    lang_code = 'de'
  elif 'en' in file_name:
    lang_code = 'en'

  
  json_str = '[' + input_string.replace('\n', '')


  json_str = json_str.replace('\"', '')
  json_str = json_str.replace('\t', '')
  json_str = json_str.replace('undefined', '\'\'')
  json_str = json_str.replace('\'', '\"')



  json_str = json_str.replace('id:', '\"id\":')
  json_str = json_str.replace('userName:', '\"userName\":')
  json_str = json_str.replace('userImage:', '\"userImage\":')
  json_str = json_str.replace('date:', '\"date\":')
  json_str = json_str.replace('url:', '\"url\":')
  json_str = json_str.replace('score:', '\"score\":')
  json_str = json_str.replace('title:', '\"title\":')
  json_str = json_str.replace('text:', '\"text\":')
  json_str = json_str.replace('replyDate:', '\"replyDate\":')
  json_str = json_str.replace('replyText:', '\"replyText\":')

  try:
    result = json.loads(json_str)
    result = list(map(add_data, result, len(result) * [lang_code]))
  except:
    pass
  
  return(result)

def process_app(app_id_str):
  
  file_list = glob.glob("pregnancy-apps-reviews/raw_data/*.txt")

  rows_df = []

  for file_name in file_list:
    
    if app_id_str in file_name:
      print(file_name)
      contents = []
      with open(file_name, 'r') as file_handle:
        contents = file_handle.read()

      pages = contents.split('[')

      size_before = len(rows_df)
      for page in pages:
        result = get_dictionary_list(page, file_name)
        rows_df = rows_df + result

  reviews_df = pd.DataFrame(rows_df)
  print(reviews_df.info())
  unique_ids = reviews_df[['id']].drop_duplicates().index
  print(reviews_df[reviews_df.index.isin(unique_ids)].info())
  filtered_df = reviews_df[reviews_df.index.isin(unique_ids)]
  filtered_df = filtered_df[['userName',	'language_code',	'date',	'score',	'title',	'text',	'replyDate',	'replyText']]

  filtered_df.to_csv('reviews_{}.csv'.format(app_id_str), index=False)
  
for app_id in ['com.easymobs.pregnancy', 'com.ovuline.pregnancy', 'com.babycenter.pregnancytracker']:
  process_app(app_id)
