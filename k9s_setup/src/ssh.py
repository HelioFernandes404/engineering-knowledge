"""
SSH utilities for k9s-config.

Handles SSH connections, configuration loading, remote command execution,
and file transfers via SFTP.
"""

import os
import time
from paramiko import SSHConfig, SSHClient
from paramiko.proxy import ProxyCommand
import paramiko
from typing import Dict, Any, Optional, Union, List
from .logging_config import get_logger

logger = get_logger()


def load_ssh_config(alias: str, ssh_config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load SSH configuration for a given host alias.

    Args:
        alias: SSH host alias to lookup
        ssh_config_path: Path to SSH config file (default: ~/.ssh/config)

    Returns:
        dict: SSH configuration parameters
    """
    if ssh_config_path is None:
        ssh_config_path = os.path.expanduser("~/.ssh/config")

    cfg: Dict[str, Any] = {}
    if not os.path.exists(ssh_config_path):
        return cfg

    with open(ssh_config_path) as f:
        sc = SSHConfig()
        sc.parse(f)
        cfg = dict(sc.lookup(alias))

    return cfg


def choose_first(lst: Any, default: Any = None) -> Any:
    """
    Get first element from list or return default.

    Args:
        lst: List-like object or single value
        default: Default value if list is empty

    Returns:
        First element or default
    """
    if not lst:
        return default
    if isinstance(lst, (list, tuple)):
        return lst[0]
    return lst


def make_ssh_client(
    hostname: str,
    username: str,
    key_filename: Optional[str],
    port: int,
    proxycmd: Optional[str] = None,
    timeout: int = 10,
    max_retries: int = 3
) -> SSHClient:
    """
    Create and connect an SSH client with retry logic.

    Retries connection with exponential backoff on transient failures
    (connection timeouts, refused connections, temporary errors).

    Args:
        hostname: SSH hostname to connect to
        username: SSH username
        key_filename: Path to SSH private key (optional)
        port: SSH port
        proxycmd: ProxyCommand string for jump hosts (optional)
        timeout: Connection timeout in seconds
        max_retries: Maximum number of connection attempts (default: 3)

    Returns:
        SSHClient: Connected SSH client

    Raises:
        Exception: On connection failure after all retries
    """
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connect_kwargs = dict(
        username=username,
        port=port,
        timeout=timeout,
        look_for_keys=True,
        allow_agent=True,
    )

    # key_filename may be None
    if key_filename:
        connect_kwargs["key_filename"] = key_filename

    if proxycmd:
        # paramiko proxy expects a socket-like ProxyCommand
        connect_kwargs["sock"] = ProxyCommand(proxycmd)

    # Retry with exponential backoff
    for attempt in range(1, max_retries + 1):
        try:
            logger.debug(f"SSH connection attempt {attempt}/{max_retries} to {hostname}:{port}")
            client.connect(hostname, **connect_kwargs)
            logger.debug(f"SSH connection successful on attempt {attempt}")
            return client
        except (paramiko.ssh_exception.NoValidConnectionsError,
                paramiko.ssh_exception.SSHException,
                OSError,
                TimeoutError) as e:
            if attempt == max_retries:
                logger.error(f"SSH connection failed after {max_retries} attempts: {e}")
                raise

            # Exponential backoff: 1s, 2s, 4s
            wait_time = 2 ** (attempt - 1)
            logger.warning(f"SSH connection failed (attempt {attempt}): {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)


def get_internal_ip(ssh: SSHClient) -> str:
    """
    Detect internal IPv4 address of remote host.

    Tries multiple commands to find the primary non-loopback IPv4 address.

    Args:
        ssh: Connected SSHClient instance

    Returns:
        str: Internal IPv4 address

    Raises:
        RuntimeError: If no valid internal IP is found
    """
    # Try a sequence of commands; return first non-loopback IPv4 found
    cmds = [
        "ip -4 addr show scope global | awk '/inet /{print $2}' | cut -d/ -f1 | head -n1",
        "hostname -I | awk '{print $1}'",
        "ip route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i==\"src\") print $(i+1)}' | head -n1",
    ]

    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode().strip()
        if out:
            # if command returned multiple IPs, take first token
            ip = out.split()[0]
            if ip and not ip.startswith("127.") and "." in ip:
                return str(ip)

    raise RuntimeError(
        "Could not detect internal IPv4 on remote host using tried commands."
    )


def fetch_remote_file(ssh: SSHClient, path: str, max_retries: int = 2) -> str:
    """
    Fetch file contents from remote host via SFTP with retry logic.

    Retries SFTP operations on transient failures (temporary connection issues,
    partial reads, etc).

    Args:
        ssh: Connected SSHClient instance
        path: Remote file path to read
        max_retries: Maximum number of fetch attempts (default: 2)

    Returns:
        str: File contents as string

    Raises:
        Exception: On SFTP or file read failure after all retries
    """
    for attempt in range(1, max_retries + 1):
        try:
            logger.debug(f"SFTP fetch attempt {attempt}/{max_retries}: {path}")
            sftp = ssh.open_sftp()
            try:
                with sftp.open(path, "r") as f:
                    data = f.read().decode()
                logger.debug(f"SFTP fetch successful on attempt {attempt}: {path}")
                return str(data)
            finally:
                sftp.close()
        except (OSError, IOError, paramiko.ssh_exception.SSHException) as e:
            if attempt == max_retries:
                logger.error(f"SFTP fetch failed after {max_retries} attempts: {path}: {e}")
                raise

            wait_time = 2 ** (attempt - 1)
            logger.warning(f"SFTP fetch failed (attempt {attempt}): {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
