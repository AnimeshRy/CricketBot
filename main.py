import requests
from datetime import datetime
from twilio.rest import Client

"""
-A Whatsapp Message Bot which sends message of cricket notifcation to your whatsapp number
-The whatsapp number has to be verified by twilio before setting it up
-Can only send 100 messages as the limit to cricapi is 100 per day.
-You can further schedule the the program to run daily as a batch script in windows
-For this create a notepad file, add the 'python.exe' fullpath and 'script' path and in the next line add fullpause and save it as a .bat file
-Schedule the bat file to run everyday using windows scheduler or you can run the script on your server and schedule it to run on certain intervals."""

CRIC_API = ''


class ScoreGet():
    def __init__(self, api_key):
        self.url_get_all_matches = 'https://cricapi.com/api/matches'
        self.get_score = 'https://cricapi.com/api/cricketScore'
        self.api_key = api_key
        self.unique_id = ""

    # get unique id's of the match you want
    def get_unique_id(self):
        #key = apikey

        url_param = {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, url_param)
        resp_dict = resp.json()
        uid_found = 0
        # will change the unique id if a match of India is found
        for ids in resp_dict['matches']:
            if (ids['team-1'] == "India" or ids['team-2'] == 'India' and ids['matchStarted'] == True):
                todays_date = datetime.today().strftime("%Y-%M-%D")
                #todays_date = "2020-05-26"
                # [2020-06-04,T00: 00: 00.000Z]
                if todays_date == ids['date'].split('T')[0]:
                    self.unique_id = ids['unique_id']
                    uid_found = 1
                    break
        # if not matches for india, uid flag stays -1
        if not uid_found:
            self.unique_id = -1

        send_data = self.get_score_current(self.unique_id)
        return send_data

    def get_score_current(self, unique_id):
        data = ""
        if unique_id == -1:
            data += 'No matches for India today.'
        else:
            url_params = {"apikey": self.api_key, "unique_id": unique_id}
            resp = requests.get(self.get_score, params=url_params)
            data_json = resp.json()
            # tring to get the current score
            try:
                data = "Here's the score : \n" + \
                    data_json['stat']+"\n"+data_json['score']
            except KeyError as e:
                print(e)
        return data


if __name__ == "__main__":
    score = ScoreGet(CRIC_API)
    whatsapp_message = score.get_unique_id()
    print(whatsapp_message)
    A_SID = ""
    AUTH_TOKEN = ""
    client = Client(A_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=whatsapp_message, from_='whatsapp:', to='whatsapp:')
