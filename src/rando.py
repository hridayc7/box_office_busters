import requests

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2EzYjE0YmJkYzY5MjcyZmNiMDUwZDI3M2Y3Mjc3ZCIsInN1YiI6IjY1YzZjNjQ0NjgwYmU4MDE3ZWEzNDhhMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NZeryWwYxMP1qjN0Stw33lF7cPmnJBuwmPmguIiIvMs"
}

url = "https://api.themoviedb.org/3/movie/664469?language=en-US"

response = requests.get(url, headers=headers)

# print(response.text)

url = "https://api.themoviedb.org/3/movie/664469/credits?language=en-US"


response = requests.get(url, headers=headers)

print(response.text)