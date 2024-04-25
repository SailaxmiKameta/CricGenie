import requests
from django.shortcuts import render, redirect
from .models import FavoritePlayer
from django.contrib.auth.decorators import login_required

def search_players(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name')

        # Search for player ID using first API
        search_api_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
        headers = {
            'X-RapidAPI-Key': 'b9fa4a9482msh0051404b674a43fp1398fajsn5decfeb2d616',
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
        'X-RapidAPI-Key': 'b9fa4a9482msh0051404b674a43fp1398fajsn5decfeb2d616',
        'X-RapidAPI-Host': 'cricbuzz-cricket.p.rapidapi.com'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        player_details = response.json()
        return render(request, 'players/player_details.html', {'player_details': player_details})
    except requests.exceptions.RequestException as e:
        return render(request, 'players/error.html', {'error': str(e)})
    
@login_required
def favorite_players(request):
    favorite_players = FavoritePlayer.objects.filter(user=request.user)

    # List to store player names
    player_names = []

    # Fetch player names for each favorite and store them in a list
    for favorite_player in favorite_players:
        player_details = fetch_player_details(favorite_player.player_id)
        if player_details:
            player_names.append(player_details.get("name"))

    # Zip favorite players and their corresponding names
    favorite_players_with_names = zip(favorite_players, player_names)

    return render(request, 'players/favorite_players.html', {'favorite_players_with_names': favorite_players_with_names})


def fetch_player_details(player_id):
    api_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
    headers = {
        'x-rapidapi-host': "cricbuzz-cricket.p.rapidapi.com",
        'x-rapidapi-key': "b9fa4a9482msh0051404b674a43fp1398fajsn5decfeb2d616"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        player_data = response.json()
        return player_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player details for player ID {player_id}: {e}")
        return None


@login_required
def add_remove_favorite(request, player_id):
    if request.method == 'POST':
        # Check if player is already in favorites
        is_favorite = FavoritePlayer.objects.filter(player_id=player_id, user=request.user).exists()

        if is_favorite:
            # Player is already a favorite, remove from favorites
            FavoritePlayer.objects.filter(player_id=player_id, user=request.user).delete()
        else:
            # Player is not a favorite, add to favorites
            FavoritePlayer.objects.create(
                player_id=player_id,
                user=request.user
            )

    return redirect('favorite_players')


def fetch_player_name(player_id):
    # Implement your logic to fetch the player name from an API or database
    # You can use libraries like `requests` for API calls or query your database
    # Replace this with your actual implementation (example using requests)
    import requests

    api_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"  # Replace with your API endpoint
    headers = {  # Replace with your API key and headers if necessary
        'x-rapidapi-host': "cricbuzz-cricket.p.rapidapi.com",
        'x-rapidapi-key': "b9fa4a9482msh0051404b674a43fp1398fajsn5decfeb2d616"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        player_data = response.json()
        return player_data.get("name")  # Assuming "name" is the field in the response
    else:
        # Handle failed API call (log error, return default value etc.)
        print(f"Error fetching player name: {response.status_code}")
        return "Player Name Unavailable"  # Placeholder for failed name retrieval