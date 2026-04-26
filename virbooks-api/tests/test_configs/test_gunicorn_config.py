import multiprocessing

import pytest

import src.configs.gunicorn_config as gunicorn_config


@pytest.mark.unit
class TestGunicornConfig:
    def test_bind_is_correct(self) -> None:
        assert gunicorn_config.bind == "0.0.0.0:5050"

    def test_workers_is_computed_from_cpu_count(self) -> None:
        expected_workers: int = multiprocessing.cpu_count() * 2 + 1
        assert gunicorn_config.workers == expected_workers

    def test_threads_is_2(self) -> None:
        assert gunicorn_config.threads == 2

    def test_timeout_is_120(self) -> None:
        assert gunicorn_config.timeout == 120

    def test_graceful_timeout_is_30(self) -> None:
        assert gunicorn_config.graceful_timeout == 30

    def test_accesslog_is_stdout(self) -> None:
        assert gunicorn_config.accesslog == "-"

    def test_errorlog_is_stdout(self) -> None:
        assert gunicorn_config.errorlog == "-"

    def test_loglevel_is_info(self) -> None:
        assert gunicorn_config.loglevel == "info"

    def test_proc_name_is_virbooks_api(self) -> None:
        assert gunicorn_config.proc_name == "virbooks-api"
