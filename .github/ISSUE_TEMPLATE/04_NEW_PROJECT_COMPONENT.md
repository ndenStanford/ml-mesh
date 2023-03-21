---
name: New Project Component
description: New Project Component.
title: "[PROJECT COMPONENT]: "
labels: ["project", "component"]
about: Adding a new project component to the codebase.
assignees: ""
---

### **Checklist**

- [ ] create a new folder `projects/<project name>/` with the component name (prepare, train, compile, serve or display).
- [ ] add the subfolders `src`, `tests/unit` and `tests/integration`.
- [ ] initialise the project by running the command `poetry init`.
- [ ] get a PR started from your feature branch to `stage`
- [ ] open an issue in [ml-platform](https://github.com/AirPR/ml-platform/blob/prod/.github/ISSUE_TEMPLATE/04_NEW_ECR_REPOSITORY.md) to create a new ECR repository with the name `<project name>-<component>`
- [ ] add the docker image to the github actions list in both `.github/workflows/deployment.yaml` and `.github/workflows/pull-request.yaml`:

```yaml
  run-projects:
    name: Build and Deploy Project Components.
    uses: ./.github/workflows/_projects.yaml
    needs: [run-tag, run-libs-tests, run-docker]
    strategy:
      max-parallel: 10
      matrix:
        poetry-version: ["1.3.2"]
        projects:
          # NOTE: list of project components to run
          ...

          - name: <new project>
            component: <project component>
            integration: false
            python-version: "3.8.16"
```

---
