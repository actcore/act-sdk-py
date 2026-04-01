from act_sdk.errors import ActError


def test_act_error_kind_and_message():
    err = ActError("std:not-found", "tool not found")
    assert err.kind == "std:not-found"
    assert err.message == "tool not found"
    assert str(err) == "tool not found"


def test_not_found():
    err = ActError.not_found("missing")
    assert err.kind == "std:not-found"


def test_invalid_args():
    err = ActError.invalid_args("bad arg")
    assert err.kind == "std:invalid-args"


def test_internal():
    err = ActError.internal("oops")
    assert err.kind == "std:internal"


def test_timeout():
    err = ActError.timeout("too slow")
    assert err.kind == "std:timeout"


def test_capability_denied():
    err = ActError.capability_denied("no network")
    assert err.kind == "std:capability-denied"


def test_is_exception():
    err = ActError.not_found("x")
    assert isinstance(err, Exception)
