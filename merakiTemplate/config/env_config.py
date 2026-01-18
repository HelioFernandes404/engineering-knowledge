import os


class EnvConfig:
    @staticmethod
    def get_api_key():
        return os.environ.get("API_KEY", "2c0fd1515727d5171e19dc0a15dbf565821b0d75")

    def get_network_id():
        return os.environ.get("NETWORK_ID", "L_646829496481105433")
