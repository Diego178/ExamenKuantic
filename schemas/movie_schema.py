from motor.motor_asyncio import AsyncIOMotorCursor

def entity_movie(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "name": movie["name"],
        "year": movie["year"],
        "gender": movie["gender"],
        "director": movie["director"],
        "rating": movie["rating"],
        "actors": movie["actors"]
    }
    
async def list_serial_movies(movies: AsyncIOMotorCursor) -> dict:
    movies_list = await movies.to_list(length=None)
    return [entity_movie(movie) for movie in movies_list]