document.getElementById('btnSwitch').addEventListener('click',()=>{
    if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
        document.documentElement.setAttribute('data-bs-theme','light')
        localStorage.setItem('color-theme', 'light');
    }
    else {
        document.documentElement.setAttribute('data-bs-theme','dark');
        localStorage.setItem('color-theme', 'dark');
    }
})