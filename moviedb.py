import requests

URL = "https://api.themoviedb.org/3/search/movie"
AUTH = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYWNlN2ZiYWI1ODMwMGYwODkxZjA4Y2FmN2RkZDUzZiIsInN1YiI6IjY1ZWJlZGFhYjdkMzUyMDE3YmU1M2QxNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CUDyM7jlBypQ0aXkSpA3HIOHZXg6_iDdEIP4Gl700Uo"

class MovieDB:
    def search(self, search_text):
        headers = {"Authorization": AUTH,
                   "accept": "application/json"}
        query = {"query": search_text}
        response = requests.get(url=URL, headers=headers, params=query)
        results = response.json()["results"]
        return results
