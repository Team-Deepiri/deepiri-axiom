"""Tests for ecosystem.devices."""

from ecosystem.devices import DeviceProfile, detect_device


def test_detect_device_returns_profile():
    dev = detect_device()
    assert isinstance(dev, DeviceProfile)
    assert dev.os_name
    assert dev.arch
    assert dev.cpu_count >= 1


def test_device_to_dict():
    dev = detect_device()
    d = dev.to_dict()
    assert "os_name" in d
    assert "has_nvidia_gpu" in d
    assert isinstance(d["gpu_names"], list)
