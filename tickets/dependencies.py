from fastapi import Request

from storage import Storage


async def get_storage(request: Request) -> Storage:
    return request.app.state.storage
