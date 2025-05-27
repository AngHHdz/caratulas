import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Registro Unidades a Transportar", layout="wide")

st.title("FORMATO DE CARÁTULA - Registro de Unidades a Transportar")

st.markdown("""
<style>
    .section-header {
        font-weight: bold;
        color: #34495e;
        font-size: 22px;
        margin-bottom: 10px;
    }
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1.5px solid #000;
        padding: 6px;
        text-align: center;
        font-family: monospace;
        font-size: 13px;
    }
    th {
        background-color: #d7d7d7;
        font-weight: bold;
    }
    .label-bold {
        font-weight: 600;
        font-size:16px;
        color:#34495e;
        margin-bottom:5px;
    }
    .header-section {
        font-weight: bold;
        color: white;
        background-color: #34495e;
        padding: 10px;
        margin-bottom: 10px;
        text-align: center;
        font-size: 1.1rem;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

vin_input = st.text_area("Ingrese hasta 12 códigos VIN (17 caracteres cada uno, separados por espacio):")
viaje_input = st.text_input("Número de VIAJE:")
buque_input = st.text_input("Nombre del BUQUE:")

def validar_vins(vin_text):
    vins = vin_text.strip().split()
    if len(vins) > 12:
        vins = vins[:12]
    for vin in vins:
        if len(vin) != 17:
            return False, vins
    return True, vins

valid, vins = validar_vins(vin_input)

if not valid and vin_input.strip() != "":
    st.error("Error: Cada código VIN debe tener exactamente 17 caracteres.")
    
def generar_tabla_html(vins, viaje, buque):
    viaje = viaje if viaje.strip() != "" else "-"
    buque = buque if buque.strip() != "" else "-"
    rows_html = ""
    for i in range(12):
        vin = vins[i] if i < len(vins) else "-"
        viaje_col = viaje if vin != "-" else "-"
        buque_col = buque if vin != "-" else "-"
        rows_html += f"""
        <tr>
            <td>{viaje_col}</td>
            <td>{buque_col}</td>
            <td style="font-family: monospace;">{vin}</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
        </tr>
        """
    html = f"""
    <div class="header-section">DOCUMENTACIÓN / PLANEACIÓN</div>
    <div class="header-section">PARA: JACKCOPPER</div>
    <div class="header-section">T R A N S P O R T I S T A</div>
    <table>
        <thead>
            <tr style="background:#d7d7d7;">
                <th>VIAJE</th>
                <th>BUQUE</th>
                <th>VIN</th>
                <th>DEALER</th>
                <th>RAZÓN SOCIAL</th>
                <th>DESTINO</th>
                <th>MODELO</th>
                <th>OBSERVACIONES</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    return html

st.markdown("---")
if vin_input.strip():
    html_table = generar_tabla_html(vins, viaje_input, buque_input)
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.info("Ingrese los VIN para que se genere el formato.")

def generar_pdf(vins, viaje, buque):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 10, "FORMATO DE CARÁTULA - Registro de Unidades a Transportar", ln=1, align='C')

    pdf.ln(5)
    pdf.set_fill_color(52, 73, 94)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "DOCUMENTACIÓN / PLANEACIÓN", ln=1, align='C', fill=True)

    pdf.set_fill_color(52, 73, 94)
    pdf.cell(0, 10, "PARA: JACKCOPPER", ln=1, align='C', fill=True)

    pdf.set_text_color(52, 73, 94)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "T R A N S P O R T I S T A", ln=1, align='C')

    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(215, 215, 215)
    col_widths = [25, 40, 60, 30, 45, 30, 25, 40]
    headers = ["VIAJE", "BUQUE", "VIN", "DEALER", "RAZÓN SOCIAL", "DESTINO", "MODELO", "OBSERVACIONES"]
    for i in range(len(headers)):
        pdf.cell(col_widths[i], 10, headers[i], border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 11)
    for i in range(12):
        vin = vins[i] if i < len(vins) else "-"
        viaje_col = viaje if vin != "-" else "-"
        buque_col = buque if vin != "-" else "-"
        fila = [viaje_col, buque_col, vin, "-", "-", "-", "-", "-"]
        for j, item in enumerate(fila):
            pdf.cell(col_widths[j], 10, item, border=1, align='C')
        pdf.ln()

    return pdf.output(dest='S').encode('latin1')

if st.button("Descargar PDF"):
    if not vin_input.strip():
        st.error("Ingrese los códigos VIN para descargar PDF")
    else:
        pdf_bytes = generar_pdf(vins, viaje_input, buque_input)
        st.download_button("Descargar PDF generado", data=pdf_bytes, file_name="formato_carátula.pdf", mime="application/pdf")
