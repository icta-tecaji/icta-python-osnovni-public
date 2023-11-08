def reject_loan(loan):
    if loan.amount > 250_000:
        loan.reject()

    return loan
