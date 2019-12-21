from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import dialogflow_v2
import uuid
import json

# Create your views here.


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        complete_uploaded_file_path = settings.BASE_DIR + uploaded_file_url

        text_file = open(complete_uploaded_file_path, 'r')
        lines = text_file.readlines()
        dialogs = detect_dialog_from_file(lines)
        return render(request, 'index.html', {'uploaded_file_url': complete_uploaded_file_path, "lines": lines, "dialogs": dialogs})
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def detect_dialog_from_file(lines: list):
    dialogs = list()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/boruto/Downloads/ek-dev-chatbot-lrpsys-b7b5f9645959.json"
    client = dialogflow_v2.SessionsClient()
    session = client.session_path('ek-dev-chatbot-lrpsys', uuid.uuid4().hex)
    for line in lines:
        query_input = dict()
        query_input["text"] = dict()
        query_input["text"]["text"] = line
        query_input["text"]["language_code"] = "en"
        # query_input = dialogflow_v2.types.QueryInput(text="flight status")
        response = client.detect_intent(session, query_input)
        # print(response.query_result.parameters.fields)
        query_result = response.query_result
        i = Intent()
        i.intent_name = query_result.intent.display_name
        i.text = line
        entities = dict()
        parameters = query_result.parameters.fields
        for k in parameters:
            entities[k] = str(parameters.get(k))
        i.parameters = json.dumps(entities)
        dialogs.append(i)
    return dialogs


class Intent:
    def __init__(self):
        text: str = ''
        intent_name: str = ''
        parameters: str = ''