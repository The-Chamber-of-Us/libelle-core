# Contributing to Libelle Volunteer Intake

Thank you for your interest in contributing to the Libelle Volunteer Intake project!  
This isn’t just code — it’s a living example of how aligned volunteers can build real change infrastructure together.

Our goal is to create a simple, trustworthy, and effective intake form that helps TCUS onboard volunteers with clarity and care. Every contribution helps move us closer to proving what’s possible when people, not just institutions, build tools for impact.

---

## Before You Start

**1. Read the Core Documents**  
- `README.md`: Quickstart guide for setup.  
- `docs/architecture.md`: High-level system overview.  
- PRD: Defines MVP scope and goals (linked in the README).  

**2. Check Open Issues**  
- Look at the Issues tab to see current work.  
- If you have a new idea, please open an issue first so we can discuss fit and scope.  

**3. Fork the Repository**  
- Fork the repo to your own GitHub account before making changes.  

---

## Your First Contribution (Workflow)

Clone your fork:
```bash
git clone https://github.com/your-username/libelle.git
cd libelle
```

Create a new branch (use a descriptive name):
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bug-name
```

Make your changes, keeping them well-documented and scoped.  

Run tests before committing (replace with actual test command when available):
```bash
# Example:
poetry run pytest
```

Commit and push:
```bash
git add .
git commit -m "feat: Add new feature"
git push origin feature/your-feature-name
```

Open a Pull Request (PR):  
- Target the `main` branch of `thechamberofus/libelle` repo.  
- Explain what your change does and why it’s needed.  
- Link to the issue you’re addressing (e.g., `Closes #123`).  

---

## Code Style & Standards

- **Python**: Follow PEP 8.  
- **Comments**: Use them to explain complex or non-obvious logic.  
- **Simplicity**: Prefer clarity and readability over cleverness.  

---

## TCUS-Specific Notes

- **Volunteer Ethos**: Remember this project is built by volunteers for volunteers. Be generous with documentation and kindness in reviews.  
- **Mission Alignment**: Features should support clarity, trust, and impact for volunteers and nonprofits.  
- **Transparency**: Significant design/tech decisions should be logged in the Slack decision log and/or changelog in the PRD.  

---

## Need Help?

- Open an issue with your question.  
- Reach out to project maintainers (contacts in `README.md`).  

We’re building something ambitious together. Thank you for being part of it!
