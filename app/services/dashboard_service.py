from datetime import datetime, timedelta
from typing import List

from sqlmodel import Session, select

from app.schemas.dashboard import DashboardSummary, DashboardKPIs, LowStockProduct
from app.schemas.report import SalesTimePoint
from app.services.report_service import ReportService
from app.models.product import Product
from app.models.settings import BusinessSettings

report_service = ReportService()


class DashboardService:

    def _get_today_range(self) -> tuple[datetime, datetime]:
        today = datetime.utcnow().date()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        return start, end

    def _get_last_7_days_range(self) -> tuple[datetime, datetime]:
        today = datetime.utcnow().date()
        start = today - timedelta(days=6)  # hoy y 6 días atrás
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(today, datetime.max.time())
        return start_dt, end_dt

    def _sales_over_last_7_days(
        self, session: Session, start: datetime, end: datetime
    ) -> List[SalesTimePoint]:
        """Reusa el reporte para construir la serie temporal de los últimos 7 días."""
        report = report_service.get_sales_report(session, start, end)
        return report.sales_over_time

    def _get_low_stock_products(self, session: Session) -> List[LowStockProduct]:
        """Lista de productos con stock por debajo del umbral configurado."""
        # Obtener settings (id=1)
        settings = session.get(BusinessSettings, 1)
        threshold = settings.low_stock_threshold if settings else 10

        statement = (
            select(Product)
            .where(
                Product.is_active == True,
                Product.stock <= threshold
            )
            .order_by(Product.stock.asc())
            .limit(20)
        )
        products = session.exec(statement).all()

        return [
            LowStockProduct(
                id=p.id,
                code=p.code,
                name=p.name,
                stock=p.stock
            )
            for p in products
        ]

    def get_dashboard_summary(self, session: Session) -> DashboardSummary:
        # Rango de hoy
        today_start, today_end = self._get_today_range()
        # Rango últimos 7 días
        last7_start, last7_end = self._get_last_7_days_range()

        # Reporte de hoy
        today_report = report_service.get_sales_report(session, today_start, today_end)
        today_kpis = DashboardKPIs(
            start_date=today_report.start_date,
            end_date=today_report.end_date,
            total_revenue=today_report.total_revenue,
            total_orders=today_report.total_orders,
            average_ticket=today_report.average_ticket,
        )

        # Reporte de últimos 7 días
        last7_report = report_service.get_sales_report(session, last7_start, last7_end)
        last7_kpis = DashboardKPIs(
            start_date=last7_report.start_date,
            end_date=last7_report.end_date,
            total_revenue=last7_report.total_revenue,
            total_orders=last7_report.total_orders,
            average_ticket=last7_report.average_ticket,
        )

        # Productos con bajo stock
        low_stock = self._get_low_stock_products(session)

        # Serie de ventas últimos 7 días
        sales_series = last7_report.sales_over_time

        return DashboardSummary(
            today=today_kpis,
            last_7_days=last7_kpis,
            low_stock_products=low_stock,
            sales_over_time=sales_series,
        )
