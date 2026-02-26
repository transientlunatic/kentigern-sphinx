// Import our custom CSS
import '../scss/styles.scss'

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

// Code copy buttons
import './code-copy'

// Initialise Bootstrap 5 ScrollSpy for the local TOC
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('#localtoc a').forEach(function (el) {
        el.classList.add('nav-link')
    })
    if (document.getElementById('localtoc')) {
        new bootstrap.ScrollSpy(document.body, { target: '#localtoc' })
    }
})
