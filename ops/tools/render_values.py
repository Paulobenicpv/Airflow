#!/usr/bin/env python3

import os, sys, pathlib

TEMPLATE = "ops/helm/values-prod.template.yaml"
OUT = "ops/helm/values-prod.yaml"

def main():
    namespace = os.getenv("NAMESPACE", "airflow-prod")
    image_repo = os.getenv("IMAGE_REPO", "ghcr.io/Paulobenicpv/Airflow")
    image_tag = os.getenv("IMAGE_TAG", "latest")
    vault_url = os.getenv("VAULT_URL", "https://REPLACE_VAULT_NAME.vault.azure.net/")

    t = pathlib.Path(TEMPLATE).read_text(encoding="utf-8")
    t = t.replace("{{NAMESPACE}}", namespace)
    t = t.replace("{{IMAGE_REPO}}", image_repo)
    t = t.replace("{{IMAGE_TAG}}", image_tag)
    t = t.replace("{{VAULT_URL}}", vault_url)
    pathlib.Path(OUT).write_text(t, encoding="utf-8")
    print(f"Wrote {OUT} with namespace={namespace}, image={image_repo}:{image_tag}, vault={vault_url}")

if __name__ == "__main__":
    main()