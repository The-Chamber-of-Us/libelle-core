# DevOps Playbook – Libelle  (v0.1 Draft)


This is a working draft to guide how we set up and evolve our DevOps practices as the platform develops. The goal right now is to lay a strong foundation—covering GitHub workflows, CI/CD, infrastructure planning, secrets management, and future deployment tooling.

---

1. GitHub Workflow

All development should happen in feature branches, with changes merged into 'main' through pull requests. Every pull request should be reviewed by at least one team member.

We encourage clear and consistent commit messages.

---

2. CI/CD (GitHub Actions)

We’ll use GitHub Actions to automate linting, testing, and deployment. This will help catch issues early and keep our development process reliable as the project grows.

Here’s what we’re planning so far:

- Frontend: linting, build checks, and deployment to Netlify (once frontend code is ready)
- Backend: testing, formatting checks, and API validation (to be defined)
- Terraform: optional dry-run validations if we move forward with infrastructure-as-code

We’ll start by adding a simple placeholder GitHub Action that runs on pull requests and pushes to 'main', just to validate that automation is wired up.

All workflow files will live under '.github/workflows/'.

---

3. Secrets Management

We’ll use GitHub Secrets to securely store things like API tokens, deploy keys, and Netlify credentials. These secrets can be referenced inside workflows as needed.

Later, if we scale up or start handling sensitive data, we may introduce a more robust secret management system like AWS Secrets Manager or HashiCorp Vault.

---

4. Infrastructure Planning

Right now, the infrastructure is minimal—just a GitHub repository with folder placeholders for frontend and backend. We expect to deploy the frontend using Netlify and host the backend on a cloud platform (likely AWS).


Once we have more clarity, we’ll revisit whether to define infrastructure with Terraform or manage it manually.

---

5. Local Development Setup

This section will grow once real code is in place. Eventually, it will cover:

- Frontend setup instructions (Node, React, or whichever framework we choose)
- Backend runtime and dependencies (Python, Flask, Node, etc.)
- Optional Docker setup for local dev environments

---

6. Monitoring and Logging

Once we’re closer to deployment, we’ll introduce basic logging and monitoring. For example, we may use Sentry for frontend error tracking or lightweight Prometheus-based tools for backend health.

We’ll also add CI checks that enforce code quality and catch regressions before merging.

---

7. Tooling Roadmap (Terraform, Docker, Kubernetes)

As the project matures, we’ll gradually adopt more powerful infrastructure and deployment tools. These are not required yet, but are part of the long-term DevOps vision.

### Terraform (Infrastructure as Code)

Terraform will be used to define and provision cloud infrastructure like:

- EC2 or container services for the backend
- S3 buckets, RDS databases, IAM roles
- Staging and production environments

Terraform configurations will be stored in a 'terraform/' directory and integrated with GitHub Actions for linting, formatting, and planning on pull requests.

### Docker (Containerization)

Docker will be used to containerize the backend so it can run consistently across developer machines and cloud environments. This will help with:

- Local development and testing
- Isolating dependencies
- Future deployment to Kubernetes or cloud services

We’ll add a 'Dockerfile' to the backend directory, and possibly a 'docker-compose.yml' to manage multiple services.

### Kubernetes (Deployment and Orchestration)

If the platform needs to scale significantly, we’ll consider using Kubernetes (EKS, GKE, or another managed service) to orchestrate deployments. Kubernetes will allow us to:

- Scale backend and frontend services independently
- Deploy with zero downtime
- Manage secrets, configs, and rollbacks declaratively

This would be a later-phase investment as the team grows and infrastructure becomes more complex.

---

This document is intended to evolve. As our architecture, tools, and codebase mature, we’ll continue refining this playbook to keep it useful and aligned with how we work.
