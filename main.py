import os
import requests
from dotenv import load_dotenv
from datetime import date

load_dotenv()

url = os.getenv('webhook_url')
username = os.getenv('username')
codeMessage = input("Enter code :\n")
# term = input("Enter Spotify Playlist ID :\n")
term = os.getenv('playlist_ID')
codeMessage = codeMessage.strip()
playlistItems = []


def getPlaylist(codeMessage: str) -> list:
    # curl -X "GET" "https://api.spotify.com/v1/playlists/37i9dQZEVXcSxqhwJP7ky3?market=IN" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
    endpoint = "https://api.spotify.com/v1/playlists/{}?market=IN".format(term)
    reqHeader = {'Authorization': 'Bearer {}'.format(
        codeMessage), 'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.get(endpoint, headers=reqHeader)

    if r.status_code in [200, 201]:
        total = r.json()['tracks']['total']
        for i in range(total):
            item = r.json()['tracks']['items'][i]['track']['uri']
            playlistItems.append(item)
    else:
        print("Sorry, an error encountered while processing your request. Traceback: \n Error {} \n {}".format(
            r.status_code, r.json()))
    return playlistItems


def getuserID(codeMessage: str) -> str:
    # curl -X "GET" "https://api.spotify.com/v1/me" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
    endpoint = "https://api.spotify.com/v1/me"
    reqHeader = {'Authorization': 'Bearer {}'.format(
        codeMessage), 'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.get(endpoint, headers=reqHeader)

    if r.status_code in [200, 201]:
        return r.json()['id']
    else:
        print("Sorry, an error encountered while processing your request. Traceback: \n Error {} \n {}".format(
            r.status_code, r.json()))


def createPlaylist(username: str, codeMessage: str) -> str:
    # curl -X "POST" "https://api.spotify.com/v1/users//playlists" --data "{data}" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {token}"
    name = "{}'s Discover Weekly {}".format(
        username, date.today().strftime("%d/%m"))
    user_id = getuserID(codeMessage)
    reqHeader = {'Authorization': 'Bearer {}'.format(
        codeMessage), 'Accept': 'application/json', 'Content-Type': 'application/json'}
    reqBody = {"name": '{}'.format(name),
               "description": "Automated Daily Mix using Python",
               "public": 'false'}
    r = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(
        user_id), headers=reqHeader, json=reqBody)

    if r.status_code in [200, 201]:
        return r.json()['id']
    else:
        print("Sorry, an error encountered while processing your request. Traceback: \n Error {} \n {}".format(
            r.status_code, r.json()))


def addSongs():
    # curl -X "POST" "https://api.spotify.com/v1/playlists/{}/tracks?uris={}" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer  {token}"
    playlistItems = getPlaylist(codeMessage)
    playlistID = createPlaylist(username, codeMessage)
    endpoint = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlistID)
    reqHeader = {'Authorization': 'Bearer {}'.format(
        codeMessage), 'Content-Type': 'application/json', 'Accept': 'application/json'}

    # playlistItems to a comma-separated list of values
    playlistItems = ",".join(map(str, playlistItems))

    payload = {'uris': playlistItems}

    r = requests.post(endpoint, headers=reqHeader, params=payload)

    if r.status_code in [200, 201]:
        # print(r.url)
        print("\nSuccessfully created playlist !")

        embed = {
            "description": "Automated Discover Weekly\n https://open.spotify.com/playlist/{}".format(playlistID),
            "title": "Your New Discover Weekly has arrived!"
        }

        data = {
            "content": "Hi Shourya!",
            "username": "Discover Weekly Webhook",
            "embeds": [
                embed
            ],
        }

        headers = {
            "Content-Type": "application/json"
        }

        result = requests.post(url, json=data, headers=headers)
        print(f"Webhook sent with status code {result.status_code}")

    else:
        print("Sorry, an error encountered while processing your request. Traceback: \n Error {} \n {}".format(
            r.status_code, r.json()))


addSongs()
