
import getters

def process_config(user, repo):
    def _process_config(config):
        config.update({
            "user": user,
            "repo": repo
        }) # i wish the impossible wish to update and return in a single exp...
        return config

    config = getters.get_github_json(user, repo, 'config.json')
    if config is None:
        return
    if isinstance(config, list):
        return [ _process_config(x) for x in config ]
    return [_process_config(x)]
    

def process_whitelist(user, repo):
    whitelist = getters.get_github_json(user, repo, 'whitelist.json')
    if whitelist is None:
        return
    return reduce(lambda x, y: x + y, ( process_config(**i) for i in whitelist ))
