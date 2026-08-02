from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime


def generate_report(stats, top_signals, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "SignalQUBE",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Pharmacovigilance Signal Detection Report",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b>1. Executive Summary</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "This report summarizes pharmacovigilance data analysed using the FAERS dataset. "
            "SignalQUBE identifies potential safety signals using PRR and ROR methods.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "<b>2. Dataset Overview</b>",
            styles["Heading2"]
        )
    )

    data = [
        ["Metric", "Value"],
        ["Drug Records", f"{stats['drug_records']:,}"],
        ["Reaction Records", f"{stats['reaction_records']:,}"],
        ["Unique Drugs", f"{stats['unique_drugs']:,}"],
        ["Unique Reactions", f"{stats['unique_reactions']:,}"],
    ]

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b>3. Top Drug-Reaction Signals</b>",
            styles["Heading2"]
        )
    )

    signal_table = [["Drug", "Reaction", "PRR", "ROR", "Signal"]]

    for _, row in top_signals.head(10).iterrows():

        signal_table.append([
            row["Drug"],
            row["Reaction"],
            row["PRR"],
            row["ROR"],
            row["Signal"]
        ])

    table2 = Table(signal_table)

    table2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkgreen),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
    ]))

    elements.append(table2)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b>4. Conclusion</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "The identified drug-reaction pairs represent disproportionate reporting signals "
            "within the FAERS dataset. These findings should be interpreted as statistical "
            "associations that may warrant further pharmacovigilance review and do not, by "
            "themselves, establish causality.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y %H:%M')}",
            styles["Italic"]
        )
    )

    doc.build(elements)