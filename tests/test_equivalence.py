import ape
import eth_utils

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

def test_token_has_name(dasy, ref):
    assert dasy.name() == ref.name()

def test_token_has_symbol(dasy, ref):
    assert dasy.symbol() == ref.symbol()

def test_balance_of(dasy, ref, owner, receiver):
    dasy.mint(receiver, 1, sender=owner)
    ref.mint(receiver, 1, sender=owner)
    assert dasy.balanceOf(receiver) == 1
    assert ref.balanceOf(receiver) == 1

def test_balance_of_reverts_zero_address(dasy, ref):
    with ape.reverts("Zero address"):
        dasy.balanceOf(ZERO_ADDRESS)

    with ape.reverts("Zero address"):
        ref.balanceOf(ZERO_ADDRESS)

def test_owner_of(dasy, ref, owner, receiver):
    dasy.mint(receiver, 1, sender=owner)
    assert dasy.ownerOf(1) == receiver

    ref.mint(receiver, 1, sender=owner)
    assert ref.ownerOf(1) == receiver

def test_owner_of_reverts_not_minted(dasy, ref):
    with ape.reverts("Not minted"):
        dasy.ownerOf(1)

    with ape.reverts("Not minted"):
        ref.ownerOf(1)

def test_mint_reverts_zero_address(dasy, ref, owner):
    with ape.reverts("Invalid receiver"):
        dasy.mint(ZERO_ADDRESS, 1, sender=owner)

    with ape.reverts("Invalid receiver"):
        ref.mint(ZERO_ADDRESS, 1, sender=owner)

def test_mint_reverts_already_minted(dasy, ref, owner, receiver):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Already minted"):
        dasy.mint(receiver, 1, sender=owner)

    ref.mint(receiver, 1, sender=owner)
    with ape.reverts("Already minted"):
        ref.mint(receiver, 1, sender=owner)

def test_mint_emits_transfer_event(dasy, ref, owner, receiver):
    tx = dasy.mint(receiver, 1, sender=owner)
    logs = list(tx.decode_logs(dasy.Transfer))
    assert len(logs) == 1
    assert logs[0].sender == ZERO_ADDRESS
    assert logs[0].receiver == receiver
    assert logs[0].tokenId == 1

    tx = ref.mint(receiver, 1, sender=owner)
    logs = list(tx.decode_logs(ref.Transfer))
    assert len(logs) == 1
    assert logs[0].sender == ZERO_ADDRESS
    assert logs[0].receiver == receiver
    assert logs[0].tokenId == 1

def test_transfer_reverts_wrong_owner(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Wrong owner"):
        dasy.transferFrom(other, other, 1, sender=other)

    ref.mint(receiver, 1, sender=owner)
    with ape.reverts("Wrong owner"):
        ref.transferFrom(other, other, 1, sender=other)

def test_transfer_reverts_zero_receiver(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Invalid receiver"):
        dasy.transferFrom(receiver, ZERO_ADDRESS, 1, sender=other)

    ref.mint(receiver, 1, sender=owner)
    with ape.reverts("Invalid receiver"):
        ref.transferFrom(receiver, ZERO_ADDRESS, 1, sender=other)

def test_transfer_reverts_not_approved(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Not approved"):
        dasy.transferFrom(receiver, other, 1, sender=other)

    ref.mint(receiver, 1, sender=owner)
    with ape.reverts("Not approved"):
        ref.transferFrom(receiver, other, 1, sender=other)

def test_transfer_updates_balances(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    dasy.transferFrom(receiver, other, 1, sender=receiver)
    assert dasy.balanceOf(receiver) == 0
    assert dasy.balanceOf(other) == 1

    ref.mint(receiver, 1, sender=owner)
    ref.transferFrom(receiver, other, 1, sender=receiver)
    assert ref.balanceOf(receiver) == 0
    assert ref.balanceOf(other) == 1

def test_transfer_updates_ownership(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    dasy.transferFrom(receiver, other, 1, sender=receiver)
    assert dasy.ownerOf(1) == other

    ref.mint(receiver, 1, sender=owner)
    ref.transferFrom(receiver, other, 1, sender=receiver)
    assert ref.ownerOf(1) == other

def test_approved_transfer(dasy, ref, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.approve(operator, 1, sender=receiver)
    dasy.transferFrom(receiver, other, 1, sender=operator)
    assert dasy.ownerOf(1) == other

    ref.mint(receiver, 1, sender=owner)
    ref.approve(operator, 1, sender=receiver)
    ref.transferFrom(receiver, other, 1, sender=operator)
    assert ref.ownerOf(1) == other

def test_approved_all_transfer(dasy, ref, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.setApprovalForAll(operator, True, sender=receiver)
    dasy.transferFrom(receiver, other, 1, sender=operator)
    assert dasy.ownerOf(1) == other

    ref.mint(receiver, 1, sender=owner)
    ref.setApprovalForAll(operator, True, sender=receiver)
    ref.transferFrom(receiver, other, 1, sender=operator)
    assert ref.ownerOf(1) == other

def test_transfer_clears_approval(dasy, ref, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.approve(operator, 1, sender=receiver)
    assert dasy.getApproved(1) == operator
    dasy.transferFrom(receiver, other, 1, sender=receiver)
    assert dasy.getApproved(1) == ZERO_ADDRESS

    ref.mint(receiver, 1, sender=owner)
    ref.approve(operator, 1, sender=receiver)
    assert ref.getApproved(1) == operator
    ref.transferFrom(receiver, other, 1, sender=receiver)
    assert ref.getApproved(1) == ZERO_ADDRESS

def test_transfer_emits_transfer_event(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    tx = dasy.transferFrom(receiver, other, 1, sender=receiver)
    logs = list(tx.decode_logs(dasy.Transfer))
    assert len(logs) == 1
    assert logs[0].sender == receiver
    assert logs[0].receiver == other
    assert logs[0].tokenId == 1

    ref.mint(receiver, 1, sender=owner)
    tx = ref.transferFrom(receiver, other, 1, sender=receiver)
    logs = list(tx.decode_logs(ref.Transfer))
    assert len(logs) == 1
    assert logs[0].sender == receiver
    assert logs[0].receiver == other
    assert logs[0].tokenId == 1

def test_safe_transfer_reverts_unsafe_receiver(dasy, ref, owner, receiver, unsafe_receiver):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Unsafe receiver"):
        dasy.safeTransferFrom(receiver, unsafe_receiver, 1, "".encode('utf-8'), sender=receiver)

    ref.mint(receiver, 1, sender=owner)
    with ape.reverts("Unsafe receiver"):
        ref.safeTransferFrom(receiver, unsafe_receiver, 1, "".encode('utf-8'), sender=receiver)

def test_safe_transfer_safe_receiver(dasy, ref, owner, receiver, safe_receiver):
    dasy.mint(receiver, 1, sender=owner)
    dasy.safeTransferFrom(receiver, safe_receiver, 1, "".encode('utf-8'), sender=receiver)
    assert dasy.ownerOf(1) == safe_receiver

    ref.mint(receiver, 1, sender=owner)
    ref.safeTransferFrom(receiver, safe_receiver, 1, "".encode('utf-8'), sender=receiver)
    assert ref.ownerOf(1) == safe_receiver

def test_set_approval_for_all(dasy, ref, owner, operator):
    dasy.setApprovalForAll(operator, True, sender=owner)
    assert dasy.isApprovedForAll(owner, operator)

    ref.setApprovalForAll(operator, True, sender=owner)
    assert ref.isApprovedForAll(owner, operator)

def test_set_approval_for_all_emits_event(dasy, ref, owner, operator):
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

    approve = ref.setApprovalForAll(operator, True, sender=owner)
    logs = list(approve.decode_logs(ref.ApprovalForAll))
    assert len(logs) == 1
    assert logs[0].owner == owner
    assert logs[0].operator == operator
    assert logs[0].isApproved == True

    revoke = ref.setApprovalForAll(operator, False, sender=owner)
    logs = list(revoke.decode_logs(ref.ApprovalForAll))
    assert len(logs) == 1
    assert logs[0].owner == owner
    assert logs[0].operator == operator
    assert logs[0].isApproved == False

def test_approve(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    dasy.approve(other, 1, sender=receiver)
    assert dasy.getApproved(1) == other

    ref.mint(receiver, 1, sender=owner)
    ref.approve(other, 1, sender=receiver)
    assert ref.getApproved(1) == other

def test_approve_approved_for_all(dasy, ref, owner, receiver, other, operator):
    dasy.mint(receiver, 1, sender=owner)
    dasy.setApprovalForAll(operator, True, sender=receiver)
    dasy.approve(other, 1, sender=operator)
    assert dasy.getApproved(1) == other

    ref.mint(receiver, 1, sender=owner)
    ref.setApprovalForAll(operator, True, sender=receiver)
    ref.approve(other, 1, sender=operator)
    assert ref.getApproved(1) == other

def test_approve_reverts_unapproved(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    with ape.reverts("Not approved"):
        dasy.approve(other, 1, sender=other)

    ref.mint(receiver, 1, sender=owner)
    with ape.reverts("Not approved"):
        ref.approve(other, 1, sender=other)

def test_approve_emits_approval_event(dasy, ref, owner, receiver, other):
    dasy.mint(receiver, 1, sender=owner)
    tx = dasy.approve(other, 1, sender=receiver)
    logs = list(tx.decode_logs(dasy.Approval))
    assert len(logs) == 1
    assert logs[0].owner == receiver
    assert logs[0].approved == other
    assert logs[0].tokenId == 1

    ref.mint(receiver, 1, sender=owner)
    tx = ref.approve(other, 1, sender=receiver)
    logs = list(tx.decode_logs(ref.Approval))
    assert len(logs) == 1
    assert logs[0].owner == receiver
    assert logs[0].approved == other
    assert logs[0].tokenId == 1

def test_supported_interfaces(dasy, ref):
    assert dasy.supportsInterface("0x01ffc9a7")
    assert dasy.supportsInterface("0x80ac58cd")
    assert dasy.supportsInterface("0x5b5e139f")
    assert dasy.supportsInterface("0xdeadbeef") == False

    assert ref.supportsInterface("0x01ffc9a7")
    assert ref.supportsInterface("0x80ac58cd")
    assert ref.supportsInterface("0x5b5e139f")
    assert ref.supportsInterface("0xdeadbeef") == False

def test_token_uri(dasy, ref):
    assert dasy.tokenURI(1) == "https://example.com/metadata/1"
    assert dasy.tokenURI(2) == "https://example.com/metadata/2"
    assert dasy.tokenURI(3) == "https://example.com/metadata/3"

def test_contract_uri(dasy, ref):
    assert dasy.contractURI() == "https://example.com/metadata/contract.json"
