function validarFormulario(event) {
    // Obtener todos los valores de los campos
    const hostname = document.querySelector('#hostname').value.trim();
    const codigoSys = document.querySelector('#codigo_sys').value.trim();
    const numeroSecuencia = document.querySelector('#numero_secuencia').value.trim();
    const fechaInicio = document.querySelector('#fecha_hora_inicio').value.trim();
    const fechaFin = document.querySelector('#fecha_hora_fin').value.trim();
    const subsistema = document.querySelector('#subsistema').value.trim();
    const nivel = document.querySelector('#nivel').value.trim();
    const tipoEvento = document.querySelector('#tipo_evento').value.trim();

    // Comprobar si todos los campos están vacíos
    if (
        hostname === '' &&
        codigoSys === '' &&
        numeroSecuencia === '' &&
        fechaInicio === '' &&
        fechaFin === '' &&
        subsistema === '' &&
        nivel === '' &&
        tipoEvento === ''
    ) {
        event.preventDefault(); // Detener el envío
        alert('Debe llenar al menos un campo del formulario.');
        return;
    }

    // Comprobar que ambas fechas estén llenas o vacías
    if ((fechaInicio === '' && fechaFin !== '') || (fechaInicio !== '' && fechaFin === '')) {
        event.preventDefault(); // Detener el envío
        alert('Debe llenar ambos campos de fecha o dejarlos vacíos.');
        return;
    }

    // Comprobar que la fecha "Desde" no sea mayor que la fecha "Hasta"
    if (fechaInicio !== '' && fechaFin !== '') {
        const fechaInicioObj = new Date(fechaInicio);
        const fechaFinObj = new Date(fechaFin);

        if (fechaInicioObj > fechaFinObj) {
            event.preventDefault(); // Detener el envío
            alert('La fecha "Desde" no puede ser mayor que la fecha "Hasta".');
            return;
        }
    }

    // Si pasa todas las validaciones, el formulario se enviará
}
