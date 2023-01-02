import ape
import eth_utils

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

def test_token_has_name(dasy):
    assert dasy.name() ==  "Mintable NFT"

def test_token_has_symbol(dasy):
    assert dasy.symbol() ==  "NFT"

def test_balance_of(dasy, owner, receiver):
    dasy.mint(receiver, 1, sender=owner)
    assert dasy.balanceOf(receiver) == 1

def test_balance_of_reverts_zero_address(dasy):
    with ape.reverts("Zero address"):
        dasy.balanceOf(ZERO_ADDRESS)

def test_owner_of(dasy, owner, receiver):
    dasy.mint(receiver, 1, sender=owner)
    assert dasy.ownerOf(1) == receiver

def test_owner_of_reverts_not_minted(dasy):
    with ape.reverts("Not minted"):
        dasy.ownerOf(1)

def test_mint_reverts_zero_address(dasy, owner):
    with ape.reverts("Invalid receiver"):
        dasy.mint(ZERO_ADDRESS, 1, sender=owner)

def test_mint_reverts_already_minted(dasy, owner, receiver):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Already minted"):
        dasy.mint(receiver, 1, sender=owner)

def test_mint_emits_transfer_event(dasy, owner, receiver):
    tx = dasy.mint(receiver, 1, sender=owner)
    logs = list(tx.decode_logs(dasy.Transfer))
    assert len(logs) == 1
    assert logs[0].sender == ZERO_ADDRESS
    assert logs[0].receiver == receiver
    assert logs[0].tokenId == 1

def test_transfer_reverts_wrong_owner(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Wrong owner"):
        dasy.transferFrom(other, other, 1, sender=other)

def test_transfer_reverts_zero_receiver(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Invalid receiver"):
        dasy.transferFrom(receiver, ZERO_ADDRESS, 1, sender=other)

def test_transfer_reverts_not_approved(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Not approved"):
        dasy.transferFrom(receiver, other, 1, sender=other)

def test_transfer_updates_balances(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    dasy.transferFrom(receiver, other, 1, sender=receiver)
    assert dasy.balanceOf(receiver) == 0
    assert dasy.balanceOf(other) == 1

def test_transfer_updates_ownership(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    dasy.transferFrom(receiver, other, 1, sender=receiver)
    assert dasy.ownerOf(1) == other

def test_approved_transfer(dasy, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.approve(operator, 1, sender=receiver)
    dasy.transferFrom(receiver, other, 1, sender=operator)
    assert dasy.ownerOf(1) == other

def test_approved_all_transfer(dasy, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.setApprovalForAll(operator, True, sender=receiver)
    dasy.transferFrom(receiver, other, 1, sender=operator)
    assert dasy.ownerOf(1) == other

def test_transfer_clears_approval(dasy, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.approve(operator, 1, sender=receiver)
    assert dasy.getApproved(1) == operator
    dasy.transferFrom(receiver, other, 1, sender=receiver)
    assert dasy.getApproved(1) == ZERO_ADDRESS

def test_transfer_emits_transfer_event(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    tx = dasy.transferFrom(receiver, other, 1, sender=receiver)
    logs = list(tx.decode_logs(dasy.Transfer))
    assert len(logs) == 1
    assert logs[0].sender == receiver
    assert logs[0].receiver == other
    assert logs[0].tokenId == 1

def test_safe_transfer_reverts_unsafe_receiver(dasy, owner, receiver, unsafe_receiver):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Unsafe receiver"):
        dasy.safeTransferFrom(receiver, unsafe_receiver, 1, "".encode('utf-8'), sender=receiver)

def test_safe_transfer_safe_receiver(dasy, owner, receiver, safe_receiver):
    dasy.mint(receiver, 1, sender=owner)
    dasy.safeTransferFrom(receiver, safe_receiver, 1, "".encode('utf-8'), sender=receiver)
    assert dasy.ownerOf(1) == safe_receiver

def test_set_approval_for_all(dasy, owner, operator):
    dasy.setApprovalForAll(operator, True, sender=owner)
    assert dasy.isApprovedForAll(owner, operator)

def test_set_approval_for_all_emits_event(dasy, owner, operator):
    approve = dasy.setApprovalForAll(operator, True, sender=owner)
    logs = list(approve.decode_logs(dasy.ApprovalForAll))
    assert len(logs) == 1
    assert logs[0].owner == owner
    assert logs[0].operator == operator
    assert logs[0].isApproved == True

    revoke = dasy.setApprovalForAll(operator, False, sender=owner)
    logs = list(revoke.decode_logs(dasy.ApprovalForAll))
    assert len(logs) == 1
    assert logs[0].owner == owner
    assert logs[0].operator == operator
    assert logs[0].isApproved == False

def test_approve(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    dasy.approve(other, 1, sender=receiver)
    assert dasy.getApproved(1) == other

def test_approve_approved_for_all(dasy, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.setApprovalForAll(operator, True, sender=receiver)
    dasy.approve(other, 1, sender=operator)
    assert dasy.getApproved(1) == other

def test_approve_reverts_unapproved(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Not approved"):
        dasy.approve(other, 1, sender=other)

def test_approve_emits_approval_event(dasy, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    tx = dasy.approve(other, 1, sender=receiver)
    logs = list(tx.decode_logs(dasy.Approval))
    assert len(logs) == 1
    assert logs[0].owner == receiver
    assert logs[0].approved == other
    assert logs[0].tokenId == 1

def test_supported_interfaces(dasy):
    assert dasy.supportsInterface("0x01ffc9a7")
    assert dasy.supportsInterface("0x80ac58cd")
    assert dasy.supportsInterface("0x5b5e139f")
    assert dasy.supportsInterface("0xdeadbeef") == False

def test_token_uri(dasy):
    assert dasy.tokenURI(1) == "https://example.com/metadata/1"
    assert dasy.tokenURI(2) == "https://example.com/metadata/2"
    assert dasy.tokenURI(3) == "https://example.com/metadata/3"

def test_contract_uri(dasy):
    assert dasy.contractURI() == "https://example.com/metadata/contract.json"
