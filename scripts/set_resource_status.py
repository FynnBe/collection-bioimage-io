import json
from pathlib import Path

import typer
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


def main(
    collection_folder: Path,
    id_: str,
    version_ids: str = typer.Argument(..., help="json string of list of dois"),
    status: str = typer.Argument(..., help="status to set"),
    only_if_pending: bool = True,
) -> int:
    version_ids = json.loads(version_ids)
    resource_path = collection_folder / id_ / "resource.yaml"
    resource = yaml.load(resource_path)
    for v in resource["versions"]:
        if v["version_id"] in version_ids:
            if not only_if_pending or (only_if_pending and v["status"] == "pending"):
                v["status"] = status

    if any(v["status"] == "accepted" for v in resource["versions"]):
        resource_status = "accepted"
    elif any(v["status"] == "pending" for v in resource["versions"]):
        resource_status = "pending"
    else:
        resource_status = "blocked"

    resource["status"] = resource_status

    yaml.dump(resource, resource_path)

    return 0


if __name__ == "__main__":
    typer.run(main)
