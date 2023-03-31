# wakatime stats

> Check out the dashboard here -> [wakatime.abhin.dev](https://wakatime.abhin.dev/)

## How it works?

### daily cron

A daily cronjob runs at 00:05 am (GMT) which fetches all the wakatime stats for the previous day for a set of Wakatime API Keys stored in environment variables. After fetching, it stores them as a JSON in logs folder. The workflow then commits the file into the main branch using Github Bot.

_Check [Github Workflow](./.github/workflows/fetch-stats.yaml), [main.py](./main.py)_

### react dashboard

On a push to the production (main) branch, a deployment on Vercel is triggered for the dashboard which is hosted at [wakatime.abhin.dev](https://wakatime.abhin.dev/)

_Check [react-app](./react-app/)_
