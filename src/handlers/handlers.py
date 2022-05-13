import jsonschema

from aiohttp.web import Request, Response, RouteTableDef
from src.handlers.schemas import AGREGATE_SCHEMA


routes = RouteTableDef()


@routes.post("/agregate")
async def agregate(request: Request):
    body = await request.json()

    try:
        jsonschema.validate(body, AGREGATE_SCHEMA)
    except jsonschema.exceptions.ValidationError as exc:
        return Response(text=f"Validation error: {str(exc)}", status=400)

    return Response(text="Hello, world")
