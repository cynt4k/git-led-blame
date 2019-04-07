import requests

class GitlabHelper():
    # self.base_url: str
    # self.auth_key: str

    def __init__(self, base_url: str, project_id: int, auth_key: str):
        self.base_url = base_url
        self.auth_key = auth_key
        self.project_id = project_id


    def get_project(self) -> dict:
        data = dict()
        header = {'PRIVATE-TOKEN': self.auth_key}
        url = self.base_url + '/projects/' + str(self.project_id)
        r = requests.get(url, headers=header)

        if r.ok:
            data = r.json()
            return data
        else:
            raise Exception('Error while getting data')

    def get_pipelines(self, branch=None) -> list:
        data = list()
        header = {'PRIVATE-TOKEN': self.auth_key}
        r = requests.get(self.base_url + '/projects/' + str(self.project_id) + '/pipelines', headers=header)

        if r.ok:
            data = r.json()
        else:
            raise Exception('Error while getting data')

        if branch:
            data = list(filter(lambda entry: entry['ref'] == branch, data))
        return data

    def get_pipeline(self, id: int) -> dict:
        data = dict()
        header = {'PRIVATE-TOKEN': self.auth_key}
        url = self.base_url + '/projects/' + str(self.project_id) + '/pipelines/' + str(id)
        r = requests.get(url, headers=header)

        if r.ok:
            data = r.json()
            return data
        else:
            raise Exception('Error while getting data')

    def get_last_failed(self, branch=None) -> dict:
        failed = dict()

        try:
            if branch:
                pipelines = self.get_pipelines(branch=branch)
            else:
                pipelines = self.get_pipelines()
            filter_func = lambda pipeline: pipeline['status'] == 'failed'
            data = list(filter(filter_func, pipelines))
            # failed = filter(lambda pipeline: pipeline.status == 'failed', pipelines)
            if len(failed) >= 1:
                failed = self.get_pipeline(data[0].id)
            return failed
        except Exception:
            return data

    def check_if_ok(self, branch: str) -> bool:
        pipelines = self.get_pipelines(branch=branch)
        if len(pipelines) == 0:
            return True
           
        if pipelines[0]['status'] == 'failed':
            return False
        else:
            return True
