## Vault Credentials Setup

1. Create a `.vault_credentials` file in the `system/config/` folder.
2. The file should include the following variables, which can be obtained from the HashiCorp Web App:
- `HCP_CLIENT_ID`
- `HCP_CLIENT_SECRET`
- `HCP_SECRETS_URL`
3. Optionally, you can add the `LOADED` variable.
4. Run the script `run.sh` in the project root.
5. Use the following commands to manage the project:
- `build` and `up` to start the project.
- `stop` to turn off the compose environment.

This setup retrieves secrets into the `.env` file and then runs the project using Docker Compose.
