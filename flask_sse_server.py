import os
from dotenv import load_dotenv
from flask import Flask, Response, request
from model import Model


# Initialize Flask app and model
load_dotenv()
app = Flask(__name__)
api_key=os.getenv("MODEL_API_KEY", None)
if not api_key:
    raise Exception("Please add your model provider api key to the .env file.")
model = Model(api_key=api_key)


def generate_data(query):
    # Stream the response from the model
    for chunk in model.query_stream(query):
        # Yield the chunk as a data event
        # The "data:" prefix and the "\n\n" suffix are required
        yield f"data: {chunk}\n\n"


@app.route('/query')
def stream():
    query = request.get_json()["query"]

    return Response(generate_data(query), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)