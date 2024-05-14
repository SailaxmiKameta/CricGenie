class SearchPlayersMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware executed")

        # If the request method is POST and the path matches the search players URL
        if request.method == 'POST' and request.path == '/players/':
            # Log the search player request
            player_name = request.POST.get('player_name')
            print(f"Search players request for player: {player_name}")

        response = self.get_response(request)
        print("Middleware executed after view")

        return response
