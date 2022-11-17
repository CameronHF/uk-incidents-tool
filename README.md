# UK Incidents tool

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
