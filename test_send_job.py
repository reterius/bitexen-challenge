import requests
import json

request_obj = {
    "args": [10, 20]
}

flower_api_result = requests.post(
    url="http://127.0.0.1:5555/api/task/async-apply/tasks.worker_topla",
    data=json.dumps(request_obj), )

if flower_api_result.status_code not in [200, 201]:
    print("celery apiye ulaşılamadı")

res = json.loads(flower_api_result.text)

print("Celery job id: ", res['task-id'])
