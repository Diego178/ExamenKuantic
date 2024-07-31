from motor.motor_asyncio import AsyncIOMotorCursor
def entity_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        "type": user["type"]
    }

async def list_serial_users(users: AsyncIOMotorCursor) -> dict:
    users_list = await users.to_list(length=None)
    return [entity_user(user) for user in users_list]