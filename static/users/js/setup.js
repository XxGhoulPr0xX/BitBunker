document.addEventListener('DOMContentLoaded', function() { 
    document.getElementById('q').addEventListener('click', function() {
        generatePDF(1);
    });
    document.getElementById('w').addEventListener('click', function() {
        generatePDF(2);
    });
    document.getElementById('e').addEventListener('click', function() {
        generatePDF(3);
    });
});

async function loadImageBase64(url) {
    const response = await fetch(url);
    const blob = await response.blob();
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.readAsDataURL(blob);
    });
}

async function generatePDF(reportNumber) {
    let firstName = document.getElementById('firstName').value || 'Nombre';
    let middleName = document.getElementById('middleName').value || 'Apellido Paterno';
    let lastName = document.getElementById('lastName').value || 'Apellido Materno';
    let semester = document.getElementById('semester').value || 'Semestre';

    const imageContainer = document.getElementById("imageUrls");
    const imagenIzquierdaURL = imageContainer.getAttribute("data-imagen-izquierda");
    const imagenDerechaURL = imageContainer.getAttribute("data-imagen-derecha");

    const imagenIzquierdaBase64 = await loadImageBase64(imagenIzquierdaURL);
    const imagenDerechaBase64 = await loadImageBase64(imagenDerechaURL);

    const docDefinition = {
        content: [
            { text: `Reporte No. ${reportNumber}`, alignment: 'right', margin: [0, 0, 0, 10] },
            {
                columns: [
                    {
                        width: 'auto',
                        stack: [
                            { image: imagenIzquierdaBase64, width: 50, height: 50 }
                        ]
                    },
                    {
                        width: '*',
                        alignment: 'right',
                        stack: [
                            { image: imagenDerechaBase64, width: 50, height: 50 }
                        ]
                    }
                ],
                columnGap: 20,
                margin: [0, 0, 0, 10]
            },
            {
                table: {
                    widths: ['20%', '20%', '20%', '40%'],
                    body: [
                        [{ text: 'Nombre:', bold: true }, { text: `${middleName}` }, { text: `${lastName}` }, { text: `${firstName}` }],
                        [{ text: 'Apellido Paterno', colSpan: 2, alignment: 'center' }, {}, { text: 'Apellido Materno', alignment: 'center' }, { text: 'Nombre(s)', alignment: 'center' }],
                        [{ text: 'Carrera:', bold: true, colSpan: 3 }, {}, {}, { text: 'No. de Control:', bold: true }],
                    ]
                },
                margin: [0, 10, 0, 10]
            },
            {
                table: {
                    widths: ['20%', '20%', '20%', '20%', '20%'],
                    body: [
                        [{ text: 'Periodo Reportado:', colSpan: 5, bold: true }, {}, {}, {}, {}],
                        [{ text: 'Del día:', alignment: 'right' }, { text: '17' }, { text: 'mes', alignment: 'center' }, { text: 'septiembre' }, { text: 'año 2024' }],
                        [{ text: 'al día:', alignment: 'right' }, { text: '16' }, { text: 'mes', alignment: 'center' }, { text: 'noviembre' }, { text: 'año 2024' }],
                    ]
                },
                margin: [0, 0, 0, 10]
            },
            {
                text: `El presente documento certifica que el/la estudiante ${firstName} ${middleName} ${lastName} de ${semester} semestre, con número de matrícula [Número de matrícula], ha cumplido satisfactoriamente con las [Número] horas de servicio social requeridas.`,
                margin: [0, 10, 0, 0]
            }
        ],
        defaultStyle: { fontSize: 10 }
    };

    pdfMake.createPdf(docDefinition).download(`Reporte_${reportNumber}.pdf`);
}
