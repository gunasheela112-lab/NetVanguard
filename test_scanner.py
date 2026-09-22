import queue
import socket
import unittest
from unittest.mock import MagicMock, patch

from scanner import ping_host, ping_host_diagnostic, resolve_host, scan_single_port


class TestPingHost(unittest.TestCase):
    @patch("scanner.subprocess.run")
    def test_ping_host_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        self.assertTrue(ping_host("192.168.1.1"))

    @patch("scanner.subprocess.run")
    def test_ping_host_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr="timeout")
        self.assertFalse(ping_host("192.168.1.1"))

    @patch("scanner.subprocess.run")
    def test_ping_diagnostic_includes_latency(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        result = ping_host_diagnostic("192.168.1.1")
        self.assertTrue(result["reachable"])
        self.assertIsNotNone(result["latency_ms"])

    @patch("scanner.subprocess.run", side_effect=__import__("subprocess").TimeoutExpired(cmd="ping", timeout=1))
    def test_ping_diagnostic_handles_timeout(self, mock_run):
        result = ping_host_diagnostic("192.168.1.1")
        self.assertFalse(result["reachable"])
        self.assertIsNotNone(result["error"])


class TestResolveHost(unittest.TestCase):
    @patch("scanner.socket.gethostbyname", return_value="192.168.1.10")
    def test_resolve_host(self, mock_resolve):
        self.assertEqual(resolve_host("example.com"), "192.168.1.10")

    @patch("scanner.socket.gethostbyname", side_effect=socket.gaierror)
    def test_resolve_host_failure(self, mock_resolve):
        self.assertIsNone(resolve_host("invalid.example"))


class TestScanSinglePort(unittest.TestCase):
    @patch("scanner.socket.socket")
    def test_port_open(self, mock_socket_class):
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0
        mock_socket_class.return_value = mock_socket
        result_queue = queue.Queue()
        scan_single_port("192.168.1.1", 22, result_queue)
        self.assertEqual(result_queue.get()["status"], "open")
        mock_socket.close.assert_called_once()

    @patch("scanner.socket.socket")
    def test_port_closed(self, mock_socket_class):
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 1
        mock_socket_class.return_value = mock_socket
        result_queue = queue.Queue()
        scan_single_port("192.168.1.1", 22, result_queue)
        self.assertEqual(result_queue.get()["status"], "closed")

    @patch("scanner.socket.socket")
    def test_port_error(self, mock_socket_class):
        mock_socket = MagicMock()
        mock_socket.connect_ex.side_effect = OSError("network error")
        mock_socket_class.return_value = mock_socket
        result_queue = queue.Queue()
        scan_single_port("192.168.1.1", 22, result_queue)
        result = result_queue.get()
        self.assertEqual(result["status"], "error")
        self.assertIn("network error", result["error"])


if __name__ == "__main__":
    unittest.main()
