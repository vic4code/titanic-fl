import os
from pipeline.backend.pipeline import PipeLine

pipeline_upload = PipeLine().set_initiator(role='guest', party_id=9999).set_roles(guest=9999)
partition = 4

dense_data_guest_train = {"name": "titanic_guest_train", "namespace": f"experiment"}
dense_data_host_train = {"name": "titanic_host_train", "namespace": f"experiment"}
dense_data_guest_validate = {"name": "titanic_guest_validate", "namespace": f"experiment"}
dense_data_host_validate  = {"name": "titanic_host_validate", "namespace": f"experiment"}


data_base = "/data/projects/fate"
pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/pipeline/titanic/data/preprocessed_titanic_train_guest.csv"),
                                table_name=dense_data_guest_train["name"],             # table name
                                namespace=dense_data_guest_train["namespace"],         # namespace
                                head=1, partition=partition)               # data info

pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/pipeline/titanic/data/preprocessed_titanic_train_host.csv"),
                                table_name=dense_data_host_train["name"],
                                namespace=dense_data_host_train["namespace"],
                                head=1, partition=partition)

pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/pipeline/titanic/data/preprocessed_titanic_validate_guest.csv"),
                                table_name=dense_data_guest_validate["name"],             # table name
                                namespace=dense_data_guest_validate["namespace"],         # namespace
                                head=1, partition=partition)               # data info

pipeline_upload.add_upload_data(file=os.path.join(data_base, "examples/pipeline/titanic/data/preprocessed_titanic_validate_host.csv"),
                                table_name=dense_data_host_validate["name"],
                                namespace=dense_data_host_validate["namespace"],
                                head=1, partition=partition)


pipeline_upload.upload(drop=1)