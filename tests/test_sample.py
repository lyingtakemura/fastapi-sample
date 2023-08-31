import pytest

@pytest.fixture(scope='module')
def sample_fixture():
    return [x for x in range(10)]

class TestSample:  # group related tests
    @pytest.mark.xfail()
    def test_fail(self):
        assert (1, 2) == (2, 1)

    def test_traceback(self):
        __tracebackhide__ = True  # hide traceback if test fails
        assert 2 in [2, 3]
        if not 2 in [2, 3]:
            pytest.fail("NOT_FOUND")

    def test_type_error(self):
        with pytest.raises(TypeError):  # test fails if not raised error
            "".join(1)

    def test_fixture(self, sample_fixture):
        assert 0 in sample_fixture


@pytest.mark.parametrize(["x", "y"], [(5, 6), (7, 8)])
def test_parametrize_function(x, y):
    assert sum([x, y]) > 10


@pytest.mark.skip()
def test_skip():
    assert 1 == 2