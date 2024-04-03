import logging
import os
from posixpath import abspath
import subprocess
from tempfile import SpooledTemporaryFile
import time
from typing import Iterable
from remotebmi.client.client import RemoteBmiClient
from remotebmi.client.utils import DeadContainerException, get_unique_port

class BmiClientApptainer(RemoteBmiClient):
    def __init__(self, image: str, work_dir: str, input_dirs: Iterable[str] = tuple(), delay=0, 
                 capture_logs=True,
                 ):
        if type(input_dirs) == str:
            msg = f'type of argument "input_dirs" must be collections.abc.Iterable; ' \
                  f'got {type(input_dirs)} instead'
            raise TypeError(msg)
        host = 'localhost'
        port = get_unique_port(host)
        args = [
            "apptainer",
            "run",
            "--contain",
            "--env", f"BMI_PORT={port}"
        ]

        for raw_input_dir in input_dirs:
            input_dir = abspath(raw_input_dir)
            if not os.path.isdir(input_dir):
                raise NotADirectoryError(input_dir)
            args += ["--bind", f'{input_dir}:{input_dir}:ro']
        self.work_dir = abspath(work_dir)
        if self.work_dir in {abspath(d) for d in input_dirs}:
            raise ValueError('Found work_dir equal to one of the input directories. Please drop that input dir.')
        if not os.path.isdir(self.work_dir):
            raise NotADirectoryError(self.work_dir)
        args += ["--bind", f'{self.work_dir}:{self.work_dir}:rw']
        # Change into working directory
        args += ["--pwd", self.work_dir]
        args.append(image)
        logging.info(f'Running {image} apptainer container on port {port}')
        if capture_logs:
            self.logfile = SpooledTemporaryFile(max_size=2 ** 16,  # keep until 65Kb in memory if bigger write to disk
                                                prefix='grpc4bmi-apptainer-log',
                                                mode='w+t',
                                                encoding='utf8')
            stdout = self.logfile
        else:
            stdout = subprocess.DEVNULL
        self.container = subprocess.Popen(args, preexec_fn=os.setsid, stderr=subprocess.STDOUT, stdout=stdout)
        time.sleep(delay)
        returncode = self.container.poll()
        if returncode is not None:
            raise DeadContainerException(
                f'apptainer container {image} prematurely exited with code {returncode}',
                returncode,
                self.logs()
            )
        url = f'http://{host}:{port}'
        super(BmiClientApptainer, self).__init__(url)


    def __del__(self):
        if hasattr(self, "container"):
            self.container.terminate()
            self.container.wait()
        if hasattr(self, "logfile"):
            # Force deletion of log file
            self.logfile.close()

    def logs(self) -> str:
        """Returns complete combined stdout and stderr written by the Apptainer container.

        When object was created with `log_enable=False` argument then always returns empty string.
        """
        if not hasattr(self, "logfile"):
            return ''

        current_position = self.logfile.tell()
        # Read from start
        self.logfile.seek(0)
        content = self.logfile.read()
        # Write from last position
        self.logfile.seek(current_position)
        return content