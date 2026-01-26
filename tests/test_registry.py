
from epiagent.tools.registry import get_registry, EpiversePackage

def test_registry_loading():
    """Test that the registry loads correctly."""
    registry = get_registry()
    assert len(registry.packages) > 0, "Registry should contain packages"

def test_package_serialization():
    """Test EpiversePackage creation and serialization."""
    package = EpiversePackage(
        name="test-package",
        organization="test-org",
        summary="Test package for validation",
        category="r_package",
        topics=["test", "validation"]
    )
    
    data = package.to_dict()
    assert data["name"] == "test-package"
    assert data["organization"] == "test-org"
    assert data["category"] == "r_package"
    assert "test" in data.get("topics", [])
