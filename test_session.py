#import pytest
import pytest

from session import add_numbers

def test_add_positive():
	assert add_numbers(1,2) == 3