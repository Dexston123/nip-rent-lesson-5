from src.manager import Manager
from src.models import Parameters, Bill, TenantSettlement

def test_tenant_settlement_shares():
    parameters = Parameters()
    manager = Manager(parameters)

    manager.apartments['apart-share'] = manager.apartments.get('apart-polanka')

    manager.tenants['tenant-1'] = manager.tenants.get('tenant-1')
    manager.tenants['tenant-1'].apartment = 'apart-share'
    manager.tenants['tenant-2'] = manager.tenants.get('tenant-2')
    manager.tenants['tenant-2'].apartment = 'apart-share'
    manager.tenants['tenant-3'] = manager.tenants.get('tenant-3')
    manager.tenants['tenant-3'].apartment = 'apart-share'

    manager.bills.append(Bill(
        apartment='apart-share',
        date_due='2025-01-05',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=300.0,
        type='electricity'
    ))

    settlements = manager.create_tenant_settlements('apart-share', 2025, 1)
    
    assert len(settlements) == 3
    cost_per_tenant = 300.0 / 3

    for s in settlements:
        assert isinstance(s, TenantSettlement)
        assert s.tenant in ['tenant-1', 'tenant-2', 'tenant-3']
        assert s.apartment_settlement == 'apart-share'
        assert s.year == 2025
        assert s.month == 1
        assert s.bills_pln == cost_per_tenant
        assert s.rent_pln == manager.tenants[s.tenant].rent_pln
        assert s.total_due_pln == s.rent_pln + s.bills_pln
        assert s.balance_pln == 0.0

    manager.apartments['apart-empty'] = manager.apartments.get('apart-polanka')
    settlements_empty = manager.create_tenant_settlements('apart-empty', 2025, 1)
    assert settlements_empty == []

    manager.apartments['apart-single'] = manager.apartments.get('apart-polanka')
    manager.tenants['tenant-single'] = manager.tenants.get('tenant-1')
    manager.tenants['tenant-single'].apartment = 'apart-single'

    manager.bills.append(Bill(
        apartment='apart-single',
        date_due='2025-01-10',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=200.0,
        type='water'
    ))

    settlements_single = manager.create_tenant_settlements('apart-single', 2025, 1)
    assert len(settlements_single) == 1
    s = settlements_single[0]
    assert s.tenant == 'tenant-single'
    assert s.apartment_settlement == 'apart-single'
    assert s.year == 2025
    assert s.month == 1
    assert s.bills_pln == 200.0
    assert s.rent_pln == manager.tenants[s.tenant].rent_pln
    assert s.total_due_pln == s.rent_pln + s.bills_pln
    assert s.balance_pln == 0.0