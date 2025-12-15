from app.schemas.calculation import CalculationReport
from datetime import datetime

def test_report_empty():
    report = CalculationReport(
        total_calculations=0,
        average_operands=0.0,
        most_common_type="N/A",
        last_calculation_at=None
    )
    assert report.total_calculations == 0
    assert report.average_operands == 0.0
    assert report.most_common_type == "N/A"
    assert report.last_calculation_at is None

def test_report_typical():
    now = datetime.utcnow()
    report = CalculationReport(
        total_calculations=5,
        average_operands=2.4,
        most_common_type="addition",
        last_calculation_at=now
    )
    assert report.total_calculations == 5
    assert abs(report.average_operands - 2.4) < 1e-6
    assert report.most_common_type == "addition"
    assert report.last_calculation_at == now
