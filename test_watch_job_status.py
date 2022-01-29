import requests
import json

celery_job_id = "0d517474-36c7-48a6-811e-64fac7f11027"

flower_api_result = requests.get(
    url="http://127.0.0.1:5555/api/task/info/" + celery_job_id)

if flower_api_result.status_code not in [200, 201]:
    print("celery apiye ulaşılamadı")

res = json.loads(flower_api_result.text)

print(res)
