Install::

    virtualenv sandbox
    python setup.py install

Run::

    cd /var/local/project-root
    manage runserver
    manage shell
    etc..


Deploy::

    cp fabfile.py.sample fabfile.py # configure `project_root` and `host_string`

    tsocks fab deploy:target=production
    tsocks fab restart:target=production

Check status::

    tsocks fab status:target=production
