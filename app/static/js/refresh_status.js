// refresh status of a service
function refreshStatus(serviceId) {
    document.getElementById(`status-${serviceId}`).innerHTML = `
    <div class="spinner-border spinner-border-sm text-white" role="status">
        <span class="sr-only"></span>
    </div>
    `;
    fetch(`/check_service/${serviceId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == 'up') {
                document.getElementById(`status-${serviceId}`).classList.remove('badge', 'text-bg-danger');
                document.getElementById(`status-${serviceId}`).classList.add('badge', 'text-bg-success');
                document.getElementById(`status-${serviceId}`).innerText = "up";
            } else if (data.status == 'down') {
                document.getElementById(`status-${serviceId}`).classList.remove('badge', 'text-bg-success');
                document.getElementById(`status-${serviceId}`).classList.add('badge', 'text-bg-danger');
                document.getElementById(`status-${serviceId}`).innerText = "down";
            }
            else {
                document.getElementById(`status-${serviceId}`).classList.remove('badge', 'text-bg-success');
                document.getElementById(`status-${serviceId}`).classList.add('badge', 'text-bg-warning');
                document.getElementById(`status-${serviceId}`).innerText = "n/q";
            }
        })
        .catch(error => console.error('Error:', error));
}