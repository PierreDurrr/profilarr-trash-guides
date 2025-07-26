import os
import json
import yaml

from markdownify import markdownify


def get_file_name(profile_name):
    return profile_name.replace("[", "(").replace("]", ")")


def find_score_for_custom_format(
    trash_score_set, custom_format_name, trash_id, output_dir
):
    custom_formats_dir = os.path.join(output_dir, "..", "custom_formats")
    target_file = None
    for fname in os.listdir(custom_formats_dir):
        if fname.endswith(".yml"):
            target_file = os.path.join(custom_formats_dir, fname)
            break

        if not target_file or not os.path.exists(target_file):
            print(
                f"Custom format with trash_id {trash_id} not found in {custom_formats_dir}"
            )
            return 0

        with open(target_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or "trash_id" not in data:
            print(f"Invalid custom format data for {custom_format_name}")
            return 0

        if data["trash_id"] != trash_id:
            continue

        trash_scores = data.get("trash_scores", {})
        if not trash_scores:
            print(f"No trash scores found in {custom_format_name}")
            return 0

        return trash_scores.get(trash_score_set, trash_scores.get("default", 0))


def collect_profile_formats(trash_score_set, format_items, output_dir):
    profile_format = []
    for name, trash_id in format_items.items():
        score = find_score_for_custom_format(
            trash_score_set, name, trash_id, output_dir
        )
        if score == 0:
            continue

        profile_format.append({"name": name, "score": score})
    return profile_format


def collect_qualities(items):
    qualities = []
    quality_id = 1
    quality_collection_id = -1
    for item in items:
        if item.get("allowed", False) is False:
            continue

        quality = {
            "name": item.get("name", ""),
        }
        if item.get("items") is not None:
            quality["id"] = quality_collection_id
            quality_collection_id -= 1
            quality["description"] = ""
            quality["qualities"] = []
            for sub_item in item["items"]:
                quality["qualities"].append({"id": quality_id, "name": sub_item})
                quality_id += 1
        else:
            quality["id"] = quality_id
            quality_id += 1
        qualities.append(quality)

    return qualities


def collect_profile(service, input_json, output_dir):
    # Compose YAML structure
    name = input_json.get("name", "")
    trash_id = input_json.get("trash_id", "")
    yml_data = {
        "name": name,
        "description": f"""[Profile from TRaSH-Guides.](https://trash-guides.info/{service.capitalize()}/{service}-setup-quality-profiles)

{markdownify(input_json.get('trash_description', ''))}""".strip(),
        "trash_id": trash_id,
        "tags": [],
        "upgradesAllowed": input_json.get("upgradeAllowed", True),
        "minCustomFormatScore": input_json.get("minFormatScore", 0),
        "upgradeUntilScore": input_json.get("cutoffFormatScore", 0),
        "minScoreIncrement": input_json.get("minUpgradeFormatScore", 0),
        "qualities": collect_qualities(input_json.get("items", [])),
        "custom_formats": collect_profile_formats(
            input_json.get("trash_score_set"),
            input_json.get("formatItems", {}),
            output_dir,
        ),
        "language": input_json.get("language", "any").lower(),
    }

    # Output path
    output_path = os.path.join(output_dir, f"{get_file_name(name)}.yml")
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(yml_data, f, sort_keys=False, allow_unicode=True)
    print(f"Generated: {output_path}")


def collect_profiles(service, input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(root, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            collect_profile(service, data, output_dir)
