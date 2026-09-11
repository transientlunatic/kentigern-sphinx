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

    // Tell assistive tech which page is current in the global TOC.
    // Uses querySelectorAll because the global TOC markup is duplicated
    // (once in the mobile offcanvas, once in the desktop sidebar).
    document.querySelectorAll('#globaltoc-wrapper li.current > a.current').forEach(function (el) {
        el.setAttribute('aria-current', 'page')
    })
})
