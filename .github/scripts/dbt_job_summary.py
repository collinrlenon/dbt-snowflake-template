import os
import json
from math import floor
from typing import Dict, List, Tuple, Any

def humanize_duration(seconds: float) -> str:
    """Convert seconds to human readable duration.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string like "1 hr, 30 min, 45 sec" or "< 1 sec"
    """
    # Handle sub-second durations
    if seconds < 1:
        return "< 1 sec"
    
    # Define time units in descending order
    units = [(3600, 'hr'), (60, 'min'), (1, 'sec')]
    parts = []
    
    # Convert seconds into largest possible units
    for divisor, unit in units:
        value = floor(seconds / divisor)
        if value > 0:
            parts.append(f"{value} {unit}")
            seconds %= divisor  # Update remaining seconds
    
    return ", ".join(parts) if parts else "0 sec"

def fetch_run_results() -> Tuple[Dict[str, str], Dict[str, int], List[Dict[str, str]], str, str]:
    """Fetch and process dbt run results from environment variables and results file.
    
    Returns:
        Tuple containing:
        - run_json: Summary of the run (commit, status, duration, link)
        - status_counts: Count of successes, warnings, errors, and skips
        - filtered_results: List of errors and warnings with details
        - submitter: GitHub PR submitter username
        - comment_name: Name for the PR comment
    """
    # Map environment variable names to their keys
    env_vars = {k: os.getenv(v) for k, v in {
        'run_results': 'RUN_RESULTS',
        'run_status': 'DBT_RUN_STATUS',
        'repo': 'GITHUB_REPOSITORY',
        'submitter': 'GITHUB_PR_SUBMITTER',
        'sha': 'GITHUB_COMMIT_SHA',
        'run_id': 'GITHUB_RUN_ID',
        'comment_name': 'GITHUB_PR_COMMENT_NAME'
    }.items()}
    
    try:
        with open(env_vars['run_results'], 'r') as f:
            run = json.load(f)
            run_results = run['results']
    except Exception as e:
        print(f"Failed to read run results: {str(e)}")
        return {}, {}, [], '', ''

    # Initialize counters for different status types
    status_counts = {'successes': 0, 'warnings': 0, 'errors': 0, 'skips': 0}
    # Map various status strings to our standardized categories
    status_map = {'success': 'successes', 'pass': 'successes', 'warn': 'warnings',
                 'error': 'errors', 'fail': 'errors', 'skipped': 'skips'}
    
    # Count occurrences of each status type
    for result in run_results:
        if status := status_map.get(result['status'].lower()):
            status_counts[status] += 1

    # Prepare summary of the run
    run_json = {
        'Commit SHA': env_vars['sha'],
        'Status': env_vars['run_status'],
        'Duration': humanize_duration(float(run['elapsed_time'])),
        'Link': f"https://github.com/{env_vars['repo']}/actions/runs/{env_vars['run_id']}"
    }

    # Filter and format results that need attention (errors and warnings)
    filtered_results = [{
        'Unique ID': f"`{'.'.join(r['unique_id'].split('.')[:3]).replace('dbt_clickup.', '')}`",
        'Status': f"`{r['status'].lower()}`",
        'Message': f"```{r.get('message', '')}```"
    } for r in run_results if r['status'].lower() in ['error', 'warn', 'fail']]

    return run_json, status_counts, filtered_results, env_vars['submitter'], env_vars['comment_name']

def main() -> str:
    """Format the PR comment with run results and any alerts.
    
    Returns:
        Formatted markdown string for the PR comment
    """
    # Fetch all necessary data
    job_results, run_results, alerts, pr_submitter, comment_name = fetch_run_results()
    
    # Map job status to appropriate emoji indicators
    status_emoji = {
        'success': ':green_circle:', 
        'failure': ':red_circle:'
    }.get(job_results['Status'].lower(), ':yellow_circle:')
    
    # Build the basic summary section
    comment = [
        f"## dbt {comment_name} Summary",
        f"- Commit SHA: {job_results['Commit SHA']}",
        f"- Job Run: [link]({job_results['Link']})",
        f"- Job Duration: **`{job_results['Duration']}`**",
        f"- Job Status: {status_emoji} **`{job_results['Status']}`**",
        f"- Job Results: `{', '.join(f'{v} {k}' for k, v in run_results.items())}`",
        "---"
    ]

    # If no issues found, return early with success message
    if not alerts:
        return "\n".join(comment + ["No alerts found in the dbt PR check! :star_struck:"])

    # Process errors and warnings separately with different alert levels
    for alert_type, status_filter in [("CAUTION", ['`error`', '`fail`']), ("WARNING", ['`warn`'])]:
        if filtered_alerts := [a for a in alerts if a['Status'] in status_filter]:
            comment.append(f"\n> [!{alert_type}]")
            for alert in filtered_alerts:
                comment.append(f"> 1. **{alert['Unique ID']}**")
                comment.extend(f"    - {k}: {v}" for k, v in alert.items() if k != 'Unique ID')

    # Add final note mentioning the PR submitter
    comment.extend([
        "\n> [!IMPORTANT]",
        f"> @{pr_submitter} - Please resolve these dbt warnings/errors (if necessary) before merging this PR. :smiley:"
    ])

    return "\n".join(comment)

print(main())