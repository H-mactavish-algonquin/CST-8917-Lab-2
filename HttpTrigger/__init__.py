import azure.functions as func
import azure.durable_functions as df
import tempfile
import os


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    try:
        req_body = await req.get_body()

        # Save the uploaded image to a temporary file with the name "input"
        temp_filename = os.path.join(tempfile.gettempdir(), "input")
        with open(temp_filename, "wb") as f:
            f.write(req_body)

        client = df.DurableOrchestrationClient(context)
        instance_id = await client.start_new('Orchestrators', None, temp_filename)
        return client.create_check_status_response(req, instance_id)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
