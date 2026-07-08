from datetime import datetime


class EmailTemplate:

    @staticmethod
    def build(
        score,
        validation_results
    ):

        passed = sum(r.passed for r in validation_results)
        failed = len(validation_results) - passed

        rows = ""

        for r in validation_results:

            color = "#2ecc71" if r.passed else "#e74c3c"
            icon = "✅" if r.passed else "❌"

            rows += f"""
            <tr>
                <td>{icon}</td>
                <td>{r.rule_name}</td>
                <td>{r.column_name}</td>
                <td>{r.failed_rows}</td>
                <td style="color:{color};font-weight:bold;">
                    {"PASS" if r.passed else "FAIL"}
                </td>
            </tr>
            """

        badge_color = (
            "#27ae60"
            if score >= 95
            else "#f39c12"
            if score >= 90
            else "#e74c3c"
        )

        html = f"""
<!DOCTYPE html>
<html>

<body style="font-family:Arial;background:#f5f6fa;padding:30px;">

<div
style="
background:white;
max-width:900px;
margin:auto;
border-radius:10px;
box-shadow:0 0 15px rgba(0,0,0,.1);
padding:30px;
">

<h2>
🚨 Enterprise Data Quality Report
</h2>

<p>
Generated :
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
</p>

<h3>

Quality Score

<span
style="
background:{badge_color};
padding:8px 20px;
border-radius:20px;
color:white;
">

{score}%

</span>

</h3>

<p>

Rules Passed :
<b>{passed}</b>

<br>

Rules Failed :
<b>{failed}</b>

</p>

<table
border="1"
cellpadding="8"
cellspacing="0"
style="
border-collapse:collapse;
width:100%;
">

<tr style="background:#2c3e50;color:white;">

<th></th>

<th>Rule</th>

<th>Column</th>

<th>Failed Rows</th>

<th>Status</th>

</tr>

{rows}

</table>

<br>

<hr>

<p style="font-size:12px;color:gray;">

Generated automatically by

Enterprise Data Quality Monitoring Platform

</p>

</div>

</body>

</html>

"""

        return html