Install::

    sudo apt-get install libcurl4-gnutls-dev libcurl4-nss-dev
    sudo apt-get install libcurl4-openssl-dev librtmp-dev
    virtualenv sandbox
    python setup.py install

Run::

    cd /var/local/project-root
    manage runserver
    manage shell
    etc..

Sync country memberships to different organisations::

    manage country_request


Deploy::

    cp fabfile.py.sample fabfile.py # configure `project_root` and `host_string`

    tsocks fab deploy:target=production
    tsocks fab restart:target=production

Check status::

    tsocks fab status:target=production
