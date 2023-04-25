---
name: New Library
description: New library checklist.
title: "[LIBRARY]: "
labels: ["library"]
about: Adding a new library to the codebase.
assignees: ""
---

### **Checklist**

- [ ] create a new folder `libs/<library name>/` with your library name.
- [ ] add the subfolders `onclusiveml/<library name>`, `onclusiveml/tests/unit` and `onclusiveml/tests/integration`.
- [ ] initialise the project by running the command `poetry init`.
- [ ] register new library in `Makefile` variable `ALL_LIBS`
- [ ] get a PR started from your feature branch to `prod`

---
