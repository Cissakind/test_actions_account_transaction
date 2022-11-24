#import pytest
from session import *

def test_high_frequency_small_interval():
	t1 = transaction('paris6', 0, 10)
	a1 = account(True, 100.0)
	resultAccount, violations = autorizador(t1, a1)

	t2 = transaction('paris7', 10, 1)
	resultAccount2, violations2 = autorizador(t2, a1)

	t3 = transaction('paris8', 30, 1)
	resultAccount3, violations3 = autorizador(t3, a1)

	assert(resultAccount3.availableLimit == 89)
	assert(violations3 == ['high_frequency_small_interval'])

def test_doubled_transaction():
	t1 = transaction('paris6', 300, 1)
	a1 = account(True, 100.0)
	resultAccount, violations = autorizador(t1, a1)

	t2 = transaction('paris6', 400, 1)
	resultAccount2, violations2 = autorizador(t2, a1)

	assert(resultAccount2.availableLimit == 99)
	assert(violations2 == ['doubled-transaction'])

def test_new_account_threshold():
	a1 = account(True, 100.0)
	t1 = transaction('paris5', 0, 91)
	resultAccount, violations = autorizador(t1, a1)

	assert(resultAccount.availableLimit == 100)
	assert(violations == ['first-transaction-above-threshold'])

def test_insufficient_limit():
	a1 = account(True, 100.0)
	t1 = transaction('paris5', 400, 10)
	autorizador(t1, a1)
	t2 = transaction('paris5', 800, 100)
	resultAccount, violations = autorizador(t2, a1)

	assert(resultAccount.availableLimit == 90)
	assert(violations == ['insufficient-limit'])


def test_not_active():
	a1 = account(False, 100.0)
	t1 = transaction('paris5', 0, 10)
	resultAccount, violations = autorizador(t1, a1)
	assert(violations == ['account-not-active'])