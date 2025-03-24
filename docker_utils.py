import docker
import subprocess

client = docker.from_env()


def stdout(cmd, err_if_empty=False):
    """
    return stdout of an exec command

    :param list[str]: command to execute, in format used by
        subprocess.run (i.e. ["ls", "-l"])
    :param boolean err_if_empty: if no stdout, throws exception
    :return: str. the stdout from the command
    """
    result = subprocess.run(cmd,
                            capture_output=True,
                            text=True)

    stdout = result.stdout
    if not stdout and err_if_empty:
        raise Exception("\nNo result from subprocess command: "
                        "{}".format(" ".join(cmd)))
    return stdout


def copy(container_name, src, dest):
    """
    copy a src file to dest on a container
    """
    if container_exists(container_name):
        stdout(["docker", "cp", src, container_name + ":" + dest])


def container_exists(container_name):
    """
    check if a Docker container of a given name exists

    :param str container_name: name of the container
    :return: True if exists, False if not
    """
    containers = client.containers.list(filters={"name": "^/" + container_name + "$"})
    # names prefixed with / hence ^/
    # https://forums.docker.com/t/how-to-filter-docker-ps-by-exact-name/2880/6
    if not containers:
        return False
    if len(containers) == 1:
        return True
    else:
        raise Exception("found multiple containers " + container_name)


def container_ip(container_name):
    """
    Get the ipv4 address of a running Docker container

    :param str container_name: name of the container
    :return: str. the ip4v address of the container
    """
    if container_exists(container_name):
        # https://stackoverflow.com/questions/43692961/how-to-get-ip-address-of-running-docker-container
        ip = stdout(["docker", "inspect", "-f",
                     "'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'",
                     container_name],
                    True)
        ip = ip.strip()
        ip = ip.strip('"')
        ip = ip.strip("'")
        return ip
    else:
        raise Exception("container {} does not exist".format(container_name))
