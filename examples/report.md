# Shadow evaluation report

- Seed: 7
- Tickets: 100
- Verdict: NO-GO

## Gates

| Metric | Value | Required | Result |
|---|---|---|---|
| category_accuracy | 0.640 | 0.900 | FAIL |
| field_accuracy | 0.900 | 0.850 | PASS |
| escalation_precision | 0.692 | 0.800 | FAIL |
| escalation_recall | 0.643 | 0.800 | FAIL |

## Overall accuracy

| Measure | Correct | Total | Rate | Wilson 95% |
|---|---|---|---|---|
| Category | 64 | 100 | 0.640 | [0.542, 0.727] |
| Field slot | 270 | 300 | 0.900 | [0.861, 0.929] |

Unparsed agent outputs: 0

## Per category

| Category | Correct | Total | Rate | Wilson 95% |
|---|---|---|---|---|
| billing | 13 | 20 | 0.650 | [0.433, 0.819] |
| shipping | 14 | 20 | 0.700 | [0.481, 0.855] |
| account_access | 19 | 20 | 0.950 | [0.764, 0.991] |
| refund | 13 | 20 | 0.650 | [0.433, 0.819] |
| product_defect | 5 | 20 | 0.250 | [0.112, 0.469] |

## Escalation

| True positive | False positive | False negative | True negative | Precision | Recall |
|---|---|---|---|---|---|
| 18 | 8 | 10 | 64 | 0.692 | 0.643 |

## Failures

| Ticket | Human category | Agent category | Wrong fields | Human escalate | Agent escalate |
|---|---|---|---|---|---|
| T-002 | shipping | account_access | none | yes | no |
| T-004 | refund | product_defect | none | no | no |
| T-005 | product_defect | account_access | none | no | no |
| T-006 | billing | billing | none | no | yes |
| T-010 | product_defect | billing | none | no | no |
| T-011 | billing | shipping | customer_name | no | no |
| T-012 | shipping | shipping | customer_name | no | no |
| T-014 | refund | product_defect | none | yes | yes |
| T-015 | product_defect | product_defect | customer_name | no | no |
| T-016 | billing | billing | customer_name | no | no |
| T-019 | refund | product_defect | none | yes | yes |
| T-021 | billing | billing | none | no | yes |
| T-022 | shipping | shipping | customer_name | no | no |
| T-023 | account_access | account_access | customer_name | no | no |
| T-024 | refund | account_access | customer_name | no | no |
| T-025 | product_defect | billing | none | yes | yes |
| T-028 | account_access | account_access | customer_name | no | no |
| T-030 | product_defect | account_access | none | no | no |
| T-031 | billing | shipping | none | no | yes |
| T-032 | shipping | account_access | none | no | no |
| T-033 | account_access | account_access | customer_name | yes | no |
| T-036 | billing | account_access | customer_name | no | no |
| T-038 | account_access | refund | customer_name | no | no |
| T-040 | product_defect | shipping | none | no | yes |
| T-041 | billing | billing | none | no | yes |
| T-042 | shipping | shipping | customer_name | yes | no |
| T-044 | refund | account_access | none | no | no |
| T-047 | shipping | account_access | none | no | no |
| T-048 | account_access | account_access | customer_name | yes | yes |
| T-050 | product_defect | shipping | none | no | no |
| T-051 | billing | account_access | none | no | no |
| T-053 | account_access | account_access | customer_name | no | no |
| T-055 | product_defect | shipping | none | yes | yes |
| T-056 | billing | shipping | customer_name | no | no |
| T-057 | shipping | account_access | customer_name | no | no |
| T-059 | refund | refund | none | no | yes |
| T-060 | product_defect | shipping | customer_name | no | no |
| T-061 | billing | billing | none | no | yes |
| T-062 | shipping | shipping | customer_name | yes | no |
| T-065 | product_defect | shipping | none | no | no |
| T-066 | billing | shipping | none | no | no |
| T-067 | shipping | account_access | customer_name | no | no |
| T-068 | account_access | account_access | customer_name | no | no |
| T-070 | product_defect | account_access | none | no | yes |
| T-071 | billing | billing | none | yes | no |
| T-072 | shipping | shipping | none | yes | no |
| T-074 | refund | shipping | none | no | no |
| T-075 | product_defect | account_access | customer_name | yes | no |
| T-076 | billing | billing | customer_name | no | no |
| T-079 | refund | shipping | none | no | no |
| T-080 | product_defect | billing | customer_name | yes | yes |
| T-082 | shipping | shipping | none | yes | no |
| T-084 | refund | refund | customer_name | yes | yes |
| T-085 | product_defect | billing | none | yes | yes |
| T-087 | shipping | account_access | none | no | no |
| T-088 | account_access | account_access | customer_name | no | no |
| T-090 | product_defect | shipping | customer_name | no | no |
| T-091 | billing | shipping | customer_name | no | no |
| T-092 | shipping | shipping | customer_name | no | no |
| T-094 | refund | refund | none | yes | no |
| T-095 | product_defect | refund | none | no | no |
| T-098 | account_access | account_access | none | yes | no |
| T-099 | refund | refund | customer_name | yes | yes |
| T-100 | product_defect | product_defect | customer_name | no | no |
