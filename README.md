# UK Incidents tool

## Web apps

### Production

The production web app is deployed manually.

To deploy it, do:
- Go to `Actions`.
- Select workflow `Streamlit web app production`.
- Click on `Run workflow`, select `Branch: master` and click on the green button `Run workflow.

[Link to production web app](https://uk-incidents-tool.dwh-k8s.hellofresh.io)
### Staging

The statging web app shows the latest changes from the master/main branch of this project.
The latest changes are auto-deployed by CI/CD pipeline.

[Link to staging web app](https://uk-incidents-tool-staging.dwh-k8s.hellofresh.io)
## Development

Here we provide information how to develop on this repo.

### Auto-format files before committing

We use `pre-commit`, which runs hooks on git actions.

To install the config file `.pre-commit-config.yaml` use these commands:
```shell
pre-commit install
pre-commit install-hooks
pre-commit install --hook-type prepare-commit-msg
```
