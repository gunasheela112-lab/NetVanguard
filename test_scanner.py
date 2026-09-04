import unittest
from unittest.mock import patch, MagicMock
import queue

from scanner import ping_host, scan_single_port


class TestPingHost(unittest.TestCase):

    @patch("scanner.subprocess.run")
    def test_ping_host_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = ping_host("192.168.1.1")
        self.assertTrue(result)

    @patch("scanner.subprocess.run")
    def test_ping_host_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        result = ping_host("192.168.1.1")
        self.assertFalse(result)


class TestScanSinglePort(unittest.TestCase):

    @patch("scanner.socket.socket")
    def test_port_open_adds_to_queue(self, mock_socket_class):
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect_ex.return_value = 0
        mock_socket_class.return_value = mock_socket_instance

        result_queue = queue.Queue()
        scan_single_port("192.168.1.1", 22, result_queue)

        self.assertFalse(result_queue.empty())
        self.assertEqual(result_queue.get(), 22)

    @patch("scanner.socket.socket")
    def test_port_closed_does_not_add_to_queue(self, mock_socket_class):
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect_ex.return_value = 1
        mock_socket_class.return_value = mock_socket_instance

        result_queue = queue.Queue()
        scan_single_port("192.168.1.1", 22, result_queue)

        self.assertTrue(result_queue.empty())


if __name__ == "__main__":
    unittest.main()
