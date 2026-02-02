# Acoular Organizational CI

## Permissions
- Permissions are set *restrictive* for the entire organization. This means that specific permissions need to be configured for every workflow.
- **Only** define permissions in `workflow.yml` if it is really necessary. E.g., `contents: read` is the default and not needed. Defining this would make it cumbersome to change defaults.

## Secrets
- We configure CI such that all secrets and access tokens are defined in environments. This allows for granular control of access. Additionally, every GitHub workflow that requires access to an environment secret should require additional approval by select accounts (not teams).

## Environments
Environments are hardcoded. Currently, there are
- `anaconda` (only master-branch, requires approval, secret token)
- `gh-pages` (only gh-pages)
- `pypi` (only master-branch, requires approval)
- `testpypi`

## Deployment
- **PyPI** and TestPyPI deployments use [trusted publishing](https://docs.pypi.org/trusted-publishers/). This means that we do not need a secret or token in GitHub. Instead, we configure a specific GitHub environment as trusted source on the PyPI side. If we select this environment in the GitHub workflow, short-lived access tokens will be generated on demand automatically.
- **Anaconda** uses an access token. The token needs to be generated on the [Anaconda website or CLI](https://www.anaconda.com/docs/tools/anaconda-org/admin-guide/tokens) (scope: "Allow all operations on Conda repositories"). It is *not* added as an organizational secret but as an environment secret to each repository. This token has en expiration date and needs to be renewed yearly.
