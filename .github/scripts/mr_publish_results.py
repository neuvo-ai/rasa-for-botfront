# Send model regression test results to Segment with a summary
# of all test results.
import analytics
import datetime
import json
import os

IS_EXTERNAL = os.environ["IS_EXTERNAL"]
DATASET_REPOSITORY_BRANCH = os.environ["DATASET_REPOSITORY_BRANCH"]
EXTERNAL_DATASET_REPOSITORY_BRANCH = None
CONFIG_REPOSITORY = "training-data"
CONFIG_REPOSITORY_BRANCH = os.environ["DATASET_REPOSITORY_BRANCH"]

analytics.write_key = os.environ["SEGMENT_TOKEN"]

task_mapping = {
    "intent_report.json": "Intent Classification",
    "CRFEntityExtractor_report.json": "Entity Prediction",
    "DIETClassifier_report.json": "Entity Prediction",
    "response_selection_report.json": "Response Selection",
    "story_report.json": "Story Prediction",
}


def send_to_segment(context):
    global IS_EXTERNAL
    global DATASET_REPOSITORY_BRANCH

    jobID = os.environ["GITHUB_RUN_ID"]

    analytics.identify(
        jobID, {"name": "model-regression-tests", "created_at": datetime.datetime.now()}
    )

    if str(IS_EXTERNAL).lower() in ("yes", "true", "t", "1"):
        IS_EXTERNAL = True
        DATASET_REPOSITORY_BRANCH = os.environ["EXTERNAL_DATASET_REPOSITORY_BRANCH"]
    else:
        IS_EXTERNAL = False

    analytics.track(
        jobID,
        "results",
        {
            "dataset": os.environ["DATASET_NAME"],
            "dataset_repository_branch": DATASET_REPOSITORY_BRANCH,
            "external_dataset_repository": IS_EXTERNAL,
            "config_repository": CONFIG_REPOSITORY,
            "config_repository_branch": CONFIG_REPOSITORY_BRANCH,
            "dataset_repository_branch": os.environ["DATASET_REPOSITORY_BRANCH"],
            "dataset_commit": os.environ["DATASET_COMMIT"],
            "workflow": os.environ["GITHUB_WORKFLOW"],
            "config": os.environ["CONFIG"],
            "pr_url": os.environ["PR_URL"],
            "accelerator_type": os.environ["ACCELERATOR_TYPE"],
            "test_run_time": os.environ["TEST_RUN_TIME"],
            "train_run_time": os.environ["TRAIN_RUN_TIME"],
            "total_run_time": os.environ["TOTAL_RUN_TIME"],
            "github_run_id": os.environ["GITHUB_RUN_ID"],
            "github_sha": os.environ["GITHUB_SHA"],
            "github_event": os.environ["GITHUB_EVENT_NAME"],
            "type": os.environ["TYPE"],
            **context,
        },
    )


def read_results(file):
    with open(file) as json_file:
        data = json.load(json_file)

        keys = ["accuracy", "weighted avg", "macro avg", "micro avg", "conversation_accuracy"]
        result = {key: data[key] for key in keys if key in data}

    return result


def push_results(file_name, file):
    result = read_results(file)
    result["file_name"] = file_name
    result["task"] = task_mapping[file_name]
    send_to_segment(result)


if __name__ == "__main__":
    for dirpath, dirnames, files in os.walk(os.environ["RESULT_DIR"]):
        for f in files:
            if any(f.endswith(valid_name) for valid_name in task_mapping.keys()):
                push_results(f, os.path.join(dirpath, f))
    analytics.flush()
