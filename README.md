# python-web-app
## Python FastAPI Web App 
### How to run locally

0. install poetry, python project management tool
1. cd to project root
2. issue `poetry install` for setup
3. `poetry run uvicorn --host 0.0.0.0 --port 8080 eventapp.__main__:app --reload`

### How to test
#### unit test
- `poetry run pytest`

### API DOC

Please check `controller.py` and `models/user.py` for details.
Swagger is provided at URL: /redoc

## Tanzu Application Platform

### Sample create app command

```
$ tanzu apps workload create tz-eventapp \
-a tz-eventapp \
--annotation autoscaling.knative.dev/minScale=1 \
--annotation autoscaling.knative.dev/maxScale=1 \
--git-repo https://github.com/yuichi110/tz_eventapp \
--git-branch main \
--type web \
--yes \
--namespace demo
```