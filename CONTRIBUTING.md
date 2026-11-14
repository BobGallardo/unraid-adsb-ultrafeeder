# Contributing

1. Open the repository in VS Code and create a feature branch (`git switch -c feature/name`).
2. Make small, reviewable changes to `templates/adsb-ultrafeeder.xml` and documentation.
3. Run `python scripts/validate.py`, or the VS Code task **Validate Unraid XML template**.
4. Test the template in Unraid's Docker UI. Include your Unraid version, image tag, logs, and what you verified in the pull request. Redact coordinates, device serials, private hostnames, and credentials.
5. Do not enable remote data-sharing in the generic template without an explicit discussion.
6. Open a pull request to `main`. At least one reviewer should check template permissions and defaults.

This project maintains an Unraid template, not the upstream SDR-Enthusiasts Docker image. For image defects, report to upstream after isolating the problem.
