# dbt-Snowflake Template

[![dbt Version](https://img.shields.io/badge/dbt-orange.svg?logo=dbt)](https://github.com/dbt-labs/dbt-core)
[![Snowflake](https://img.shields.io/badge/snowflake-blue.svg?logo=snowflake)](https://www.snowflake.com/)

A production-ready template for deploying dbt projects with Snowflake using GitHub Actions. This template provides a streamlined setup process and includes essential features for reliable data transformations.

**Prerequisites**
- GitHub account
- Snowflake account
- Basic understanding of dbt and Snowflake
l
## 📚 Table of Contents
- [Setup](#setup)
  - [1. Using This Template](#1-using-this-template)
  - [2. Initial Configuration](#2-initial-configuration)
  - [3. Development Environment](#3-development-environment)
  - [4. GitHub Actions Deployment](#4-github-actions-deployment)
- [Functionality](#️functionality)
  - [Core Features](#core-features)
  - [Security](#security)
- [How does it work under-the-hood?](#how-does-it-work-under-the-hood)
  - [Environment Variables](#environment-variables)
  - [Job Summary PR Comment](#job-summary-pr-comment)
  - [PR Schema Cleanup](#pr-schema-cleanup)
  - [Manifest Writeback](#manifest-writeback)
  - [Adhoc Job Workflow](#adhoc-job-workflow)
  - [Snowflake RBAC](#snowflake-rbac)

## 🚀 Setup

### 1. Using This Template

1. Click the "**Use this template**" button at the top of this repository
2. Name your repository and select visibility (public/private)

### 2. Initial Configuration

1. Set up GitHub Secrets
   - The account, admin user, and admin password were created when you created your Snowflake account, so just copy them here
   - The rest of the credentials have not been created yet, so define them below and they will propagate to Snowflake once we setup RBAC
   - It might be more efficient to fill these creds in the `example.env` file and then copy them from there into Github
   - Go to your new repository's `Settings` > `Secrets and variables` > `Actions`
     - Under `Secrets` > `New repository secret`, add a new secret for each of the following:
       - `SNOWFLAKE_ACCOUNT`: Should be in this format (ex. `abcdefg-abc12345`)
       - `SNOWFLAKE_ADMIN_USER`: The username you initially created
       - `SNOWFLAKE_ADMIN_PASSWORD`: The password you initially created
       - `SNOWFLAKE_GITHUB_PASSWORD`: Newly-defined password that Snowflake will use to create your github user
       - `SNOWFLAKE_DBT_PASSWORD`: Newly-defined password that Snowflake will use to create your dbt user
       - `SNOWFLAKE_HEX_PASSWORD`: Newly-defined password that Snowflake will use to create your Hex (bi tool) user
     - Under `Variables` > `New repository variable`, add a new variable for each of the following:
       - `SNOWFLAKE_GITHUB_USER`: Newly-defined username that Snowflake will use to create your github user
         - This can be renamed to whatever tool you're going to use for ingestion
       - `SNOWFLAKE_DBT_USER`: Newly-defined username that Snowflake will use to create your dbt user
       - `SNOWFLAKE_HEX_USER`: Newly-defined username that Snowflake will use to create your Hex user
         - This can be renamed to whatever tool you're going to use for BI
       - `SNOWFLAKE_PRODUCTION_DATABASE`: Newly-defined database that you will use to hold productionized data (I use the name `production`)
       - `SNOWFLAKE_PR_DATABASE`: Newly-defined database that you will use to hold data from dbt PR checks (I use the name `beta`)
       - `SNOWFLAKE_DEVELOPEMNT_DATABASE`: Newly-defined database that you will use to hold local development data (I use the name `development`)
       - `SNOWFLAKE_RAW_DATABASE`: Newly-defined database that you will use to hold raw data ingested from various sources (I use the name `raw`)

2. Configure Snowflake credentials
   - Run the "**Snowflake RBAC Job**" GitHub Action workflow to automatically:
     - Create necessary databases, warehouses, roles, and users
     - Set up required access permissions
   - Monitor the progress in your repository's Actions tab

### 3. Development Environment

1. **Clone your repository**
   - Clone your new repository locally:
     - **Recommended**: Clone via SSH
     - For instructions on enabling SSH, [see GitHub's guide for creating SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)

2. **Make template adjustments**
   - Update profile name in `profiles.yml` from `dbt_template` to something more applicable
   - Update project name in `dbt_project.yml` from `dbt_template` to something more applicable
     - Don't forget to update the name under the `seeds` and `models` sections as well
   - Uncomment and adjust GitHub Action schedule for daily job as preferred:
     - `.github/workflows/dbt_daily_job.yml`
   - Uncomment the GitHub Action `push` event trigger for merge job:
     - `.github/workflows/dbt_merge_job.yml`
   - Change the `DBT_STATE` path in your `example.env` file to the full path of your artifacts repo
   - Any other adjustments as preferred

3. **Install development tools**
   ```bash
   # Install Oh My Zsh (recommended for better terminal experience)
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install GitHub CLI
   brew install gh
   gh auth login  # Follow prompts to authenticate

   # Install pipx
   brew install pipx
   ```

4. **Install dbt using pipx**
   ```bash
   # Install dbt-snowflake and dependencies, specify version
   pipx install dbt-snowflake==<version> --include-deps
   
   # Add pipx binaries to PATH
   pipx ensurepath

   # Important: After running ensurepath, run either:
   source ~/.zshrc  # if using zsh
   source ~/.bashrc # if using bash
   
   # Verify installation
   dbt --version
   ```

5. **Create and configure environment file**
   ```bash
   mv example.env .env
   # TODO: Fill the placeholder values with your credentials

   source .env # Initialize environment variables
   ```

6. **Verify Snowflake connection**
   ```bash
   dbt debug  # Should show all checks passing
   ```

7. **Initialize your development environment**
   ```bash
   dbt deps   # Install packages
   dbt build  # Run all resources
   ```

### 4. GitHub Actions Deployment

1. **Test deployment with a simple change**
   - Make a small change locally (e.g., add a comment to a model in `models/` directory)
   - Commit and push to a new branch
   ```bash
   git switch -c test/initial-deployment
   git add .
   git commit -m "test: add comment to verify deployment"
   git push -u origin test/initial-deployment    # Sets up branch tracking
   
   # Create PR using GitHub CLI
   gh pr create --title "test: verify deployment" --body "Testing initial deployment setup"
   # If you have multiple GitHub accounts, you will want to make sure you are authed into the one for this repo in order to use gh
   ```

2. **Verify PR Checks**
   - Verify the PR check Action automatically:
     - Runs dbt checks against PR database
       - On the first run, it will do a full dbt build on this first PR (not `state:modified+1`) because there is no manifest to refer to
     - Adds PR comment with affected models
     - Shows successful completion

3. **Merge PR and verify workflows**
   - Merge the PR in GitHub interface
   - Verify these Actions run successfully:
     - Schema teardown job (cleans up PR database)
     - Merge-deployment job
       - On the first run, it will do a full dbt build on this first PR (not `state:modified+`) because there is no manifest to refer to
     - Adds PR comment with affected models upon completion

4. **Test daily & adhoc jobs**
   - Manually trigger the daily job in Actions tab
   - Verify successful completion
   - Manually trigger the adhoc job in Actions tab
   - Verify successful completion

## ⚙️ Functionality

### Core Features

- **Automated Data Pipeline**
  - Scheduled and triggered jobs to run dbt resources
  - Configurable runtime parameters and schedules
  - Built-in PR templates and conventions

- **Built-in CI/CD Framework**
  - Continuous Integration
    - Automated testing in isolated PR environments
    - Impact analysis with detailed PR comments
    - Data quality and model validation checks
  - Continuous Deployment
    - Streamlined production deployments
    - Automated schema cleanup post-PR
    - State management via manifest tracking

- **Jobs Breakdown**
  - **Adhoc Job** (`dbt_adhoc_job.yml`)
    - Purpose: Allows manual running of specific dbt resources
    - Trigger: Manual trigger only

  - **Daily Job** (`dbt_daily_job.yml`)
    - Purpose: Runs full dbt build daily to ensure data freshness
    - Trigger: Scheduled to run daily (configurable)
      - Can also be triggered manually (but shouldn't need to)
  
  - **Merge Job** (`dbt_merge_job.yml`) 
    - Purpose: Runs modified models when code is merged to main branch
    - Trigger: On push to main branch (ignoring the `artifacts` directory)
      - Can also be triggered manually (but shouldn't need to)
    - Also adds PR comment with results summary

  - **PR Cleanup Job** (`dbt_pr_cleanup.yml`)
    - Purpose: Removes PR-specific schemas after PR is closed
    - Trigger: On PR close or merge

  - **PR Check Job** (`dbt_pr_job.yml`)
    - Purpose: Tests changes in isolation using PR database
    - Trigger: On pull request to main branch
    - Also adds PR comment with results summary
    
  - **Snowflake RBAC Job** (`snowflake_rbac_job.yml`)
    - Purpose: Initial Snowflake permissions/infra setup
    - Trigger: Manual trigger only
    - Should only need to run once during initial setup

### Security

- **Snowflake Integration**
  - Initial Role-based access control (RBAC) in Snowflake
  - Secure credential management via GitHub Secrets
  - Multi-environment configuration support
  - Separate environments for development, testing, and production

## 🤔 How does it work under-the-hood?

### Environment Variables
1. Created as GitHub Repository Secrets
2. Loaded into workflows as environment variables
3. Used by `profiles.yml`, Python scripts, and environment profiles

### Job Summary PR Comment
1. PR checks generate `run_results.json`
2. Python script extracts modified models, test results, and statistics
3. Results auto-posted as PR comment

### PR Schema Cleanup
1. PR checks create isolated schemas (`github_pr_{number}`)
2. On PR close/merge:
   - Cleanup workflow triggers
   - Python script drops PR schema
3. Maintains clean database environment

### Manifest Writeback
1. After merges, dbt generates `manifest.json` with project state
2. Manifest is committed to repo and saved as workflow artifact
3. Enables state comparison for selective model running

### Adhoc Job Workflow
1. Accepts inputs:
   - `command`: dbt command type
   - `selection`: optional model selection
   - `exclusion`: optional models to exclude
2. Builds command with `--target prod` and conditional flags
3. Ensures single-job execution with cancellation of in-progress runs

### Snowflake RBAC
1. Python script creates databases, warehouses, roles, and users
2. Triggered via GitHub Action with admin credentials
3. Sets up isolated environments with proper access controls