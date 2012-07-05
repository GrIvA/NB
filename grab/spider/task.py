from __future__ import absolute_import
from random import randint

from .error import SpiderMisuseError
from ..base import copy_config

class Task(object):
    """
    Task for spider.
    """

    def __init__(self, name='initial', url=None, grab=None, grab_config=None, priority=None,
                 network_try_count=0, task_try_count=0, 
                 disable_cache=False, refresh_cache=False,
                 valid_status=[], use_proxylist=True,
                 **kwargs):
        """
        Create `Task` object.

        If more than one of url, grab and grab_config options are non-empty then they
        processed in following order:
        * grab overwrite grab_config
        * grab_config overwrite url

        Args:
            :param name: name of the task. After successfull network operation
                task's result will be passed to `task_<name>` method.
            :param url: URL of network document. Any task requires `url` or `grab`
                option to be specified.
            :param grab: configured `Grab` instance. You can use that option in case
                when `url` option is not enough. Do not forget to configure `url` option
                of `Grab` instance because in this case the `url` option of `Task`
                constructor will be overwritten with `grab.config['url']`.
            :param priority: - priority of the Task. Tasks with lower priority will be
                processed earlier. By default each new task is assigned with random
                priority from (80, 100) range.
            :param network_try_count: you'll probably will not need to use it. It is used
                internally to control how many times this task was restarted due to network
                errors. The `Spider` instance has `network_try_limit` option. When
                `network_try_count` attribut of the task exceeds the `network_try_limit`
                attribut then processing of the task is abandoned.
            :param task_try_count: the as `network_try_count` but it increased only then you
                use `clone` method. Also you can set it manually. It is usefull if you want
                to restart the task after it was cacelled due to multiple network errors.
                As you might guessed there is `task_try_limit` option in `Spider` instance.
                Both options `network_try_count` and `network_try_limit` guarantee you that
                you'll not get infinite loop of restarting some task.
            :param disable_cache: if `True` disable cache subsystem. The document will be
                fetched from the Network and it will not be saved to cache.
            :param refresh_cache: if `True` the document will be fetched from the Network
                and saved to cache.
            :param valid_status: extra status codes which counts as valid
            :param use_proxylist: it means to use proxylist which was configured
                via `setup_proxylist` method of spider

            Any non-standard named arguments passed to `Task` constructor will be saved as
            attributes of the object. You can get their values later as attributes or with
            `get` method which allows to use default value if attrubute does not exist.
        """

        if name == 'generator':
            # The name "generator" is restricted because
            # `task_generator` handler could not be created because
            # this name is already used for special method which
            # generates new tasks
            raise SpiderMisuseError('Task name could not be "generator"')

        self.name = name

        if grab:
            grab_config = grab.dump_config()
        if grab_config:
            self.url = grab_config['url']
            self.grab_config = copy_config(grab_config)
        else:
            self.url = url
            self.grab_config = None

        self.priority = priority
        self.network_try_count = network_try_count
        self.task_try_count = task_try_count
        self.disable_cache = disable_cache
        self.refresh_cache = refresh_cache
        self.valid_status = valid_status
        self.use_proxylist = use_proxylist
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, key, default=None):
        """
        Return value of attribute or None if such attribute
        does not exist.
        """
        return getattr(self, key, default)

    def clone(self, **kwargs):
        """
        Clone Task instance.

        Reset network_try_count, increase task_try_count.
        """

        attr_copy = self.__dict__.copy()
        if 'grab' in attr_copy:
            del attr_copy['grab']
        task = Task(**attr_copy)

        task.network_try_count = 0
        task.task_try_count = 0

        # Carefully process url, grab, grab_config options
        url = kwargs.pop('url', None)
        grab_config = kwargs.pop('grab_config', None)
        grab = kwargs.pop('grab', None)

        if grab:
            grab_config = grab.dump_config()

        if grab_config:
            task.url = grab_config['url']
            task.grab_config = copy_config(grab_config) 
        elif url:
            task.url = url
            if task.grab_config:
                task.grab_config['url'] = url

        for key, value in kwargs.items():
            setattr(task, key, value)

        return task
