from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement

class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key, year=None, month=None):
        if apartment_key not in self.apartments and not any(bill.apartment == apartment_key for bill in self.bills):
            return None

        matching_bills = [
            bill for bill in self.bills
            if bill.apartment == apartment_key
            and (year is None or bill.settlement_year == year)
            and (month is None or bill.settlement_month == month)
        ]

        return sum(bill.amount_pln for bill in matching_bills)
    
    def create_apartment_settlement(self, apartment_key, year, month):
        bills_total = sum(
            b.amount_pln for b in self.bills
            if b.apartment == apartment_key and b.settlement_year == year and b.settlement_month == month
        )
        rent_total = sum(
            t.rent_pln for t in self.tenants.values()
            if t.apartment == apartment_key
        )
        total_due = bills_total + rent_total
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=rent_total,
            total_bills_pln=bills_total,
            total_due_pln=total_due
        )

    def create_tenant_settlements(self, apartment_key, year, month):
        apartment_settlement = self.create_apartment_settlement(apartment_key, year, month)
        tenants = [(k, t) for k, t in self.tenants.items() if t.apartment == apartment_key]
        settlements = []
        if not tenants:
            return settlements
        cost_per_tenant = apartment_settlement.total_bills_pln / len(tenants)
        for tenant_key, t in tenants:
            total_due = cost_per_tenant + t.rent_pln
            balance = t.deposit_pln - total_due
            ts = TenantSettlement(
                tenant=tenant_key,
                apartment_settlement=apartment_key,
                year=year,
                month=month,
                bills_pln=cost_per_tenant,
                rent_pln=t.rent_pln,
                total_due_pln=total_due,
                balance_pln=balance
            )
            settlements.append(ts)
        return settlements