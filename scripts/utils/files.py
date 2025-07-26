import os
import yaml


# TODO: Consider not writing these values to the file and rather keeping track in runtime
def remove_trash_references(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data.pop("trash_id", None)
    data.pop("trash_scores", None)


def clean_files(dirs):
    for dir in dirs:
        for root, _, files in os.walk(dir):
            for filename in files:
                if not filename.endswith(".yaml"):
                    continue

                file_path = os.path.join(root, filename)
                remove_trash_references(file_path)
