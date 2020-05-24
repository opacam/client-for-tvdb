base_uri = "https://api.thetvdb.com"


class EndPoints:
    """
    A class which define tvdb's api endpoints.
    """

    # Authentication (https://api.thetvdb.com/swagger#/Authentication)
    login = f"{base_uri}/login"
    refresh_token = f"{base_uri}/refresh_token"

    # Search (https://api.thetvdb.com/swagger#/Search)
    search = f"{base_uri}/search/series"

    # Series (https://api.thetvdb.com/swagger#/Series)
    series = f"{base_uri}/series"

    # Episodes (https://api.thetvdb.com/swagger#/Episodes)
    episodes = f"{base_uri}/episodes"

    # Movies (https://api.thetvdb.com/swagger#/Movies)
    movies = f"{base_uri}/movies"

    # Updates (https://api.thetvdb.com/swagger#/Updates)
    updated_query = f"{base_uri}/updated/query"
    updated_query_params = f"{base_uri}/updated/query/params"

    # Languages (https://api.thetvdb.com/swagger#/Languages)
    languages = f"{base_uri}/languages"

    # Users (https://api.thetvdb.com/swagger#/Users)
    user = f"{base_uri}/user"
    user_favorites = f"{base_uri}/user/favorites"
    user_ratings = f"{base_uri}/user/ratings"
    user_ratings_query = f"{base_uri}/user/ratings/query"
    user_ratings_query_params = f"{base_uri}/user/ratings/query/params"


end_points = EndPoints()
