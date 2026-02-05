# AutoClearance

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Automated Cross-Border Logistics Compliance System**

</div>

---

## Core Functionality

A Multi-Agent System designed to automate invoice processing and compliance auditing for logistics.

* **Zero-Shot Extraction:** Converts unstructured PDF/Image invoices into structured data using OCR + LLM.
* **Logic Verification:** Automatically audits HS Codes and validates weight consistency (Gross vs. Net).
* **ERP Integration:** Outputs standardized JSON/XML for direct system ingestion.

## Performance

| Metric | Manual Process | AutoClearance |
| :--- | :--- | :--- |
| **Processing Time** | ~20 mins / doc | **< 30 secs / doc** |
| **Method** | Manual Entry | **Automated Pipeline** |
| **Error Handling** | Human Review | **Statistical Audit** |

## Architecture

```mermaid
graph LR
    A[Raw Invoice <br> PDF/Image] --> B(Ingest Agent <br> OCR + Cleaning)
    B --> C{Auditor Agent <br> Logic Check}
    C -- Pass --> D[Delivery Agent <br> JSON Formatter]
    C -- Fail --> E[Error Report <br> Flagged Items]
    D --> F[ERP System]
