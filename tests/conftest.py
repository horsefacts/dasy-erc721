import pytest


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]

@pytest.fixture(scope="session")
def receiver(accounts):
    return accounts[1]

@pytest.fixture(scope="session")
def other(accounts):
    return accounts[2]

@pytest.fixture(scope="session")
def operator(accounts):
    return accounts[3]

@pytest.fixture(scope="session")
def metadata(owner, project):
    return owner.deploy(project.Metadata)

@pytest.fixture(scope="session")
def ref(owner, project):
    return owner.deploy(project.ERC721Reference, "Mintable NFT", "NFT")

@pytest.fixture(scope="session")
def dasy(owner, project):
    return owner.deploy(project.ERC721, "Mintable NFT", "NFT")

@pytest.fixture(scope="session")
def unsafe_receiver(owner, project):
    return owner.deploy(project.UnsafeReceiver)

@pytest.fixture(scope="session")
def safe_receiver(owner, project):
    return owner.deploy(project.SafeReceiver)
