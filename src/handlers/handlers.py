import json

import jsonschema

from aiohttp import ClientSession
from aiohttp.web import Request, Response, RouteTableDef, json_response
from src.etl.pipeline import PipelineError, pipeline
from src.handlers.schemas import AGREGATE_SCHEMA


routes = RouteTableDef()


# according to RFC, it is highly discouraged to use GET with body, so here is POST
@routes.post("/agregate")
async def agregate(request: Request):
    session: ClientSession = request.app["session"]

    try:
        body = await request.json()

        jsonschema.validate(body, AGREGATE_SCHEMA)

        result = await pipeline(session, body["account_id"], body["name"], 1)

    except jsonschema.exceptions.ValidationError as exc:
        return Response(text=f"Validation error: {str(exc)}", status=400)
    except json.decoder.JSONDecodeError:
        return Response(
            text=f"Validation error, request must to contain body", status=400
        )
    except PipelineError as exc:
        return Response(
            text=f"During query what went wrong :(. More info: {exc}", status=400
        )

    return json_response(data=result, status=200)
