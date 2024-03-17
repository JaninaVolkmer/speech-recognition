import json
import requests


class NotionClient:

    def __init__(self, token, database_id) -> None:
        self.database_id = database_id

        self.headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16"
        }

    def read_database(self):
        read_url = "https://api.notion.com/v1/databases/{database_id}/query"

        # call the API use requests module
        res = requests.post(read_url, headers=self.headers)
        # get a json object
        data = res.json()
        print(res.status_code)
        print(res.text)
        # dump data in file
        with open('./db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)

    def create_page(self, description, date, status):
        create_url = 'https://api.notion.com/v1/pages'

        # store data
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Description": {
                    "title": [
                        {
                            "text": {
                                "content": description
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                                "start": date,
                                "end": None
                            }
                },
                "Status": {
                    "rich_text": [
                        {
                            "text": {
                                "content": status
                            }
                        }
                    ]
                }
            }}

        # convert to json string - dump it to a string
        data = json.dumps(data)
        # response = do a post request to create_url, headers, data
        res = requests.post(create_url, headers=self.headers, data=data)
        # status_code needs to be 200
        print(res.status_code)
        return res

    def update_page(self, status):
        update_url = "https://api.notion.com/v1/pages/{page_id}"

        data = {
            "properties": {
                "Status": {
                    "rich_text": [
                        {
                            "text": {
                                "content": status
                            }
                        }
                    ]
                }
            }
        }

        data = json.dumps(data)
        response = requests.patch(update_url, headers=self.headers, data=data)
        print(response.status_code)
        print(response.text)
        return response
