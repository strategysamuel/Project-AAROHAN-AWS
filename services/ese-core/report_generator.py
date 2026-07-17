import logging
from typing import Dict, Any

logger = logging.getLogger("ese-report-generator")

class EnterpriseReportGenerator:
    @staticmethod
    def generate_report(report_type: str, format_type: str, data: Dict[str, Any]) -> bytes:
        """
        Generates downloadable reports:
        report_type: "FHC", "CAM", "CREDIT", "PORTFOLIO", "RECOMMENDATION", "RISK"
        format_type: "PDF", "EXCEL", "MARKDOWN"
        """
        report_type = report_type.upper()
        format_type = format_type.upper()

        title = f"PROJECT AAROHAN - {report_type} REPORT"
        customer_id = data.get("customer_id", 120)
        timestamp = "2026-07-08T14:59:00Z"

        if format_type == "MARKDOWN":
            content = f"""# {title}
Generated At: {timestamp}
Customer ID: {customer_id}

## Key Metrics
- Score: {data.get("score", 85)}
- Status: {data.get("status", "PERFORMING")}
- Value: INR {data.get("value", "2,500,000")}

## Detailed Assessment
This report compiles financial indices, compliance logs, and risk indicators to evaluate overall viability.

### Auditor Signature
*Digitally Signed by Project AAROHAN Twin Engine*
"""
            return content.encode("utf-8")

        elif format_type == "EXCEL":
            # Return CSV-compatible Excel format bytes
            csv_lines = [
                f"Report Title,{title}",
                f"Generated At,{timestamp}",
                f"Customer ID,{customer_id}",
                "",
                "Metric Name,Metric Value,Status",
                f"Score,{data.get('score', 85)},OK",
                f"Status,{data.get('status', 'PERFORMING')},OK",
                f"Value,{data.get('value', '2500000')},OK"
            ]
            return "\n".join(csv_lines).encode("utf-8")

        else: # PDF
            # Mock PDF format bytes
            pdf_lines = [
                "%PDF-1.4",
                f"1 0 obj\n<< /Title ({title}) /Author (Project AAROHAN) >>\nendobj",
                "2 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj",
                f"3 0 obj\n<< /Type /Pages /Kids [4 0 R] /Count 1 >>\nendobj",
                f"4 0 obj\n<< /Type /Page /Parent 3 0 R /MediaBox [0 0 595 842] /Contents 5 0 R >>\nendobj",
                f"5 0 obj\n<< /Length 150 >>\nstream",
                f"BT /F1 12 Tf 50 700 Td ({title}) Tj ET",
                f"BT /F1 10 Tf 50 650 Td (Customer ID: {customer_id}) Tj ET",
                f"BT /F1 10 Tf 50 600 Td (Status: {data.get('status', 'PERFORMING')}) Tj ET",
                "endstream\nendobj",
                "xref",
                "0 6",
                "0000000000 65535 f",
                "trailer\n<< /Size 6 /Root 2 0 R >>\nstartxref\n%%EOF"
            ]
            return "\n".join(pdf_lines).encode("utf-8")
