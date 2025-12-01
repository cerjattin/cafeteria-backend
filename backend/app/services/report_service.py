from datetime import datetime
from collections import Counter, defaultdict
from sqlmodel import Session
from app.repositories.order_repository import OrderRepository
from app.schemas.report import SalesReport, ReportItem, SalesTimePoint

order_repo = OrderRepository()

class ReportService:

    def get_sales_report(self, session: Session, start: datetime, end: datetime) -> SalesReport:
        orders = order_repo.list_between_dates(session, start, end)

        total_revenue = sum(o.total for o in orders)
        total_orders = len(orders)
        average_ticket = total_revenue / total_orders if total_orders > 0 else 0.0

        # top products, sales_by_category y sales_over_time dependen de productos
        from app.models.product import Product
        from app.models.order import OrderItem
        from sqlmodel import select

        product_units = Counter()
        category_units = Counter()
        time_buckets = defaultdict(float)

        for order in orders:
            for item in order.items:
                product: Product = session.get(Product, item.product_id)
                product_units[product.name] += item.qty
                category_units[product.category or "Sin categoría"] += item.qty
                # agrupar por día
                day_key = order.created_at.replace(hour=0, minute=0, second=0, microsecond=0)
                time_buckets[day_key] += item.qty * item.price

        top_products = [
            ReportItem(name=name, units=units)
            for name, units in product_units.most_common(5)
        ]

        sales_by_category = [
            ReportItem(name=cat, units=units)
            for cat, units in category_units.most_common()
        ]

        sales_over_time = [
            SalesTimePoint(timestamp=ts, total=total)
            for ts, total in sorted(time_buckets.items(), key=lambda x: x[0])
        ]

        return SalesReport(
            start_date=start,
            end_date=end,
            total_revenue=total_revenue,
            total_orders=total_orders,
            average_ticket=average_ticket,
            top_products=top_products,
            sales_by_category=sales_by_category,
            sales_over_time=sales_over_time,
        )
