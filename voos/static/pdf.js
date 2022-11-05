window.onload = function(){
    document.getElementById("download")
    .addEventListener("click", ()=>{
        const relatorio = this.document.getElementById("relatorio");
        var opt = {
            margin:1,
            filename: 'relatorio.pdf',
            image: {type: 'jpeg', quality: 0.98},
            html2canvas: {scale:2},
            jsPDF: {unit: 'in', format: 'letter', orientation: 'portrait'}
        };
        html2pdf(relatorio, opt);
    })
}