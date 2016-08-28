import json
import urllib.request

import pandas as pd

df_combined = pd.DataFrame(columns=['title', 'comment', 'rating'])
df_combined_index = 0

for page_number in range(1, 11):
    url = 'https://itunes.apple.com/rss/customerreviews/page=' \
          + str(page_number) + '/id=742044692/sortby=mostrecent/json?l=en&cc=us'
    http_response = urllib.request.urlopen(url)
    response = json.loads(http_response.read().decode('utf-8'))
    entries = response['feed']['entry']

    df = pd.DataFrame(columns=['title', 'comment', 'rating'])

    for i in range(1, len(entries)):
        row = [entries[i]['title']['label'],
               entries[i]['content']['label'].replace("\n", " "),
               entries[i]['im:rating']['label']]
        df.loc[i-1] = row
        df_combined.loc[df_combined_index] = row
        df_combined_index += 1

    df.to_csv('data' + str(page_number) + '.csv', index=False)

df_combined.to_csv('data_combined.csv', index=False)
print(df_combined.describe())
print(df_combined)





