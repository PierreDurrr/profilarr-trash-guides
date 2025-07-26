import os
import json
import yaml

from markdownify import markdownify

IMPLEMENTATION_TO_TAG_MAPPING = {
    "ReleaseTitleSpecification": ["Release Title"],
    "ResolutionSpecification": ["Resolution"],
    "SourceSpecification": ["Source"],
    "LanguageSpecification": ["Language"],
    "ReleaseGroupSpecification": ["Release Group"],
    "IndexerFlagSpecification": ["Indexer Flag"],
    "QualityModifierSpecification": ["Quality Modifier"],
    "ReleaseTypeSpecification": ["Release Type"],
}

IMPLEMENTATION_TO_TYPE_MAPPING = {
    "ReleaseTitleSpecification": "release_title",
    "ResolutionSpecification": "resolution",
    "SourceSpecification": "source",
    "LanguageSpecification": "language",
    "ReleaseGroupSpecification": "release_group",
    "IndexerFlagSpecification": "indexer_flag",
    "QualityModifierSpecification": "quality_modifier",
    "ReleaseTypeSpecification": "release_type",
}


def collect_custom_format(service, file_name, input_json, output_dir):
    conditions = []
    for spec in input_json.get("specifications", []):
        condition = {
            "name": spec.get("name", ""),
            "negate": spec.get("negate", False),
            "required": spec.get("required", False),
            "type": IMPLEMENTATION_TO_TYPE_MAPPING.get(
                spec.get("implementation"), "unknown"
            ),
        }

        implementation = spec.get("implementation")
        if implementation in ["ReleaseTitleSpecification", "ReleaseGroupSpecification"]:
            condition["pattern"] = spec.get("name", "")
        elif implementation in ["ResolutionSpecification"]:
            condition["resolution"] = f"{spec.get('fields', {}).get('value')}p"
        elif implementation in ["SourceSpecification"]:
            condition["source"] = spec.get("fields", {}).get("value")
        elif implementation in ["LanguageSpecification"]:
            # TODO: exceptLanguage
            condition["language"] = spec.get("fields", {}).get("value")
        elif implementation in ["IndexerFlagSpecification"]:
            condition["flag"] = spec.get("fields", {}).get("value")
        elif implementation in ["QualityModifierSpecification"]:
            condition["qualityModifier"] = spec.get("fields", {}).get("value")
        elif implementation in ["ReleaseTypeSpecification"]:
            condition["releaseType"] = spec.get("fields", {}).get("value")

        conditions.append(condition)

    # Compose YAML structure
    name = input_json.get("name", "")
    trash_id = input_json.get("trash_id", "")
    yml_data = {
        "name": name,
        "trash_id": trash_id,
        "trash_scores": input_json.get("trash_scores", {}),
        "description": f"""[Custom format from TRaSH-Guides.](https://trash-guides.info/{service.capitalize()}/{service.capitalize()}-collection-of-custom-formats/#{file_name})

{markdownify(input_json.get('description', ''))}""".strip(),
        "metadata": {
            "includeInRename": input_json.get("includeCustomFormatWhenRenaming", False),
        },
        "tags": IMPLEMENTATION_TO_TAG_MAPPING[implementation],
        "conditions": conditions,
        "tests": [],
    }

    # Output path
    output_path = os.path.join(output_dir, f"{file_name}.yml")
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(yml_data, f, sort_keys=False, allow_unicode=True)
    print(f"Generated: {output_path}")


def collect_custom_formats(service, input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(root, filename)
            file_stem = os.path.splitext(filename)[0]  # Filename without extension
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            collect_custom_format(service, file_stem, data, output_dir)
