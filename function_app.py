import azure.functions as func
import json
from app.managers.manager import BgRemoveManager

app = func.FunctionApp()
manager = BgRemoveManager()


@app.function_name(name="BgRemoveFunction")
@app.route(route="BgRemoveFunction", methods=["POST"])
def bg_remove(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        image_base64 = body["image_base64"]

        result_base64 = manager.remove_background(image_base64)

        return func.HttpResponse(
            json.dumps({"image_base64": result_base64}),
            mimetype="application/json",
            status_code=200,
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
        )
