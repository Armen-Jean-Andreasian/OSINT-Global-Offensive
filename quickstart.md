1. Create `.vault_credentials` file in `system/config/` folder.
2. It should include `HCP_CLIENT_ID`, `HCP_CLIENT_SECRET` and `HCP_SECRETS_URL` variables which you can obtain from the Web App of Hashicorp
3. Optionally you can add `LOADED` variable.
4. Then run the script `run.sh` in the project root.
5. `build` and `up` functions for start , and `stop` to turn off compose


This way we retrieve secrets to .env file, then run the project with compose.