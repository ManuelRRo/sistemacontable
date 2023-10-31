
const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});


window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
    }
});

const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');
        document.body.setAttribute('data-bs-theme', 'dark'); // Agrega el atributo data-bs-theme='dark'
    } else {
        document.body.classList.remove('dark');
        document.body.removeAttribute('data-bs-theme'); // Elimina el atributo data-bs-theme
    }
});