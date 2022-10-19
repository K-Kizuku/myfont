# -*- coding: utf-8 -*-
from google.cloud import aiplatform

DATA_NUM = "20"
USER_NAME = "user"

def create_custom_job(
    data_num: str, 
    user_name: str,
    project: str,
    display_name: str,
    container_image_uri: str,
    location: str = "asia-northeast1",
    api_endpoint: str = "asia-northeast1-aiplatform.googleapis.com",
):
    client_options = {"api_endpoint": api_endpoint}
    
    client = aiplatform.gapic.JobServiceClient(client_options=client_options)
    custom_job = {
        "display_name": display_name,
        "job_spec": {
            "worker_pool_specs": [
                {
                    "machine_spec": {
                        "machine_type": "n1-standard-32",
                    },
                    "replica_count": 1,
                    "container_spec": {
                        "image_uri": container_image_uri,
                        "command": [],
                        "args": [data_num, user_name],
                    },
                }
            ]
        },
    }
    parent = f"projects/{project}/locations/{location}"
    response = client.create_custom_job(parent=parent, custom_job=custom_job)
    print("response:", response)
