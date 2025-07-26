import os
import json
import yaml


def collect_regex_pattern(service, file_name, input_json, output_dir):
    # Find the first pattern in specifications
    pattern = None

    for spec in input_json.get("specifications", []):
        implementation = spec.get("implementation")
        if implementation not in [
            "ReleaseTitleSpecification",
            "ReleaseGroupSpecification",
        ]:
            continue

        pattern = spec.get("fields", {}).get("value")
        if not pattern:
            print(f"No pattern found in {file_name} for {implementation}")
            continue
        # Compose YAML structure
        name = spec.get("name", "")
        yml_data = {
            "name": name,
            "pattern": pattern,
            "description": "",
            "tags": [],
        }

        # Output path
        output_path = os.path.join(output_dir, f"{name.replace('/', '-')}.yml")
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(yml_data, f, sort_keys=False, allow_unicode=True)
        print(f"Generated: {output_path}")


def collect_regex_patterns(service, input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(root, filename)
            file_stem = os.path.splitext(filename)[0]  # Filename without extension
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            collect_regex_pattern(service, file_stem, data, output_dir)
