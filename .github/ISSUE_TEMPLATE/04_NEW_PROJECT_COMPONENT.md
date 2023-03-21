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

---
