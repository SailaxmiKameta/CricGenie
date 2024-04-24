import requests
from django.shortcuts import render

def search_players(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')

        # Search for player ID using first API
        search_api_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
        headers = {
            'X-RapidAPI-Key': '5ef9c67401msh4b6c09615e9d5b9p161c7cjsnbe3992fc2f45',
            'X-RapidAPI-Host': 'cricbuzz-cricket.p.rapidapi.com'
        }
        search_params = {"plrN": player_name}
        try:
            search_response = requests.get(search_api_url, headers=headers, params=search_params)
            search_response.raise_for_status()
            player_data = search_response.json()
            
            if player_data.get("player"):
                players_list = player_data["player"]
                return render(request, 'players/search_results.html', {'players_list': players_list})
            else:
                return render(request, 'players/search_players.html', {'error': 'Player not found'})
        except requests.exceptions.RequestException as e:
            return render(request, 'players/error.html', {'error': str(e)})
    else:
        return render(request, 'players/search_players.html')


def player_details(request, player_id):
    # SECOND API URL to fetch player details
    api_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
    headers = {
        'X-RapidAPI-Key': '5ef9c67401msh4b6c09615e9d5b9p161c7cjsnbe3992fc2f45',
        'X-RapidAPI-Host': 'cricbuzz-cricket.p.rapidapi.com'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        player_details = response.json()
        return render(request, 'players/player_details.html', {'player_details': player_details})
    except requests.exceptions.RequestException as e:
        return render(request, 'players/error.html', {'error': str(e)})