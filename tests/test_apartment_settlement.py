from src.manager import Manager
from src.models import Parameters, Bill, ApartmentSettlement

def test_apartment_settlement_balances():
    parameters = Parameters()
    manager = Manager(parameters)

    manager.apartments['apart-test'] = manager.apartments.get('apart-polanka')

    manager.bills.append(Bill(
        apartment='apart-test',
        date_due='2025-01-05',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=100.0,
        type='rent'
    ))
    manager.bills.append(Bill(
        apartment='apart-test',
        date_due='2025-01-06',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=50.0,
        type='electricity'
    ))

    manager.apartments['apart-empty'] = manager.apartments.get('apart-polanka')

    settlement_with_bills = manager.create_apartment_settlement('apart-test', 2025, 1)
    settlement_no_bills = manager.create_apartment_settlement('apart-empty', 2025, 1)

    assert isinstance(settlement_with_bills, ApartmentSettlement)
    assert settlement_with_bills.apartment == 'apart-test'
    assert settlement_with_bills.month == 1
    assert settlement_with_bills.year == 2025
    assert settlement_with_bills.total_bills_pln == 150.0
    assert settlement_with_bills.total_rent_pln == 0.0
    assert settlement_with_bills.total_due_pln == 150.0

    assert isinstance(settlement_no_bills, ApartmentSettlement)
    assert settlement_no_bills.apartment == 'apart-empty'
    assert settlement_no_bills.total_bills_pln == 0.0
    assert settlement_no_bills.total_due_pln == 0.0