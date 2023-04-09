# code stats

**Note: Project Deprecated/Unused**

## How does it work?

### 1. daily cron

A daily cronjob runs at 00:05 am (GMT) which fetches all the wakatime stats for the previous day for a set of Wakatime API Keys stored in environment variables. After fetching, it stores them as a JSON in logs folder. The workflow then commits the file into the main branch using Github Bot.

_Check [Github Workflow](./.github/workflows/fetch-stats.yaml), [main.py](./main.py)_

### 2. react dashboard (wip)

On a push to the production (main) branch, a deployment on Vercel is triggered for the dashboard which is hosted at [wakatime.abhin.dev](https://wakatime.abhin.dev/)

_Check [react-app](./react-app/)_

## other

### monthly cron

A monthly cronjob is also setup to run on the 1st of every month at 00:05 am (GMT) to compile all the stats of the previous month into 1 single file for ease of import in the react dashboard.
