import os

c = get_config()
pwd = os.path.dirname(__file__)

c.JupyterHub.spawner_class = 'mig.SwarmSpawner'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.cleanup_servers = True

# First pulls can be really slow, so let's give it a big timeout
c.SwarmSpawner.start_timeout = 60 * 10

c.SwarmSpawner.jupyterhub_service_name = 'jupyterhub'

c.SwarmSpawner.networks = ["jh_test"]

notebook_dir = os.environ.get('NOTEBOOK_DIR') or '/home/jovyan/work/'
c.SwarmSpawner.notebook_dir = notebook_dir

mounts = [{'type': 'volume',
           'driver_config': 'rasmunk/sshfs:latest',
           'driver_options': {'sshcmd': '{sshcmd}', 'id_rsa': '{id_rsa}',
                              'big_writes': '', 'allow_other': '',
                              'reconnect': '', 'port': '2222'},
           'source': 'sshvolume-user-{username}',
           'target': '/home/jovyan/work'
           }]

# 'args' is the command to run inside the service
# These are run inside every service
c.SwarmSpawner.container_spec = {
    'args': ['/usr/local/bin/start-singleuser.sh']
}

# Before the user can select which image to spawn,
# user_options has to be enabled
c.SwarmSpawner.use_user_options = True

# Available docker images the user can spawn
c.SwarmSpawner.dockerimages = [
    {'image': 'nielsbohr/base-notebook-devel:743fe46511dc',
     'name': 'Basic Python Notebook',
     'mounts': mounts}
]

# Authenticator -> remote user header
c.JupyterHub.authenticator_class = 'jhub_remote_auth_mount.MountRemoteUserAuthenticator'

# Limit cpu/mem to 4 cores/8 GB mem
# During congestion, kill random internal processes to limit
# available load to 1 core/ 2GB mem
c.SwarmSpawner.resource_spec = {
    'cpu_limit': int(8 * 1e9),
    'mem_limit': int(8192 * 1e6),
    'cpu_reservation': int(1 * 1e9),
    'mem_reservation': int(1024 * 1e6),
}

# API tokens
c.JupyterHub.api_tokens = {"tetedfgd09dg09":
                               "f5bt2rclf5jvipkoiexuypkoiexu6pkoijes6t2vhvherecl2djy6u4ylnmuxwk3lbnfweczdeojsxg4z5nvqws3caonsgm43gfzrw63i"}
