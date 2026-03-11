/**
 * Add copy buttons to code blocks
 * Handles special cases like removing $ prompts from bash/shell code
 */

function addCopyButtons() {
    // Find all code blocks
    const codeBlocks = document.querySelectorAll('div.highlight')

    codeBlocks.forEach(function (block) {
        // Skip if button already exists
        if (block.querySelector('.copy-button')) {
            return
        }

        // Create copy button
        const button = document.createElement('button')
        button.className = 'copy-button'
        button.setAttribute('type', 'button')
        button.textContent = 'Copy'
        button.setAttribute('aria-label', 'Copy code to clipboard')

        // Add click handler
        button.addEventListener('click', function () {
            copyCode(block, button)
        })

        // Add button to code block
        block.appendChild(button)
    })
}

function copyCode(block, button) {
    const pre = block.querySelector('pre')
    if (!pre) return

    // Check if this is a bash/shell/console code block
    const isBashBlock = block.classList.contains('highlight-bash') ||
                       block.classList.contains('highlight-shell')
    const isConsoleBlock = block.classList.contains('highlight-console')

    let code

    if (isConsoleBlock) {
        code = extractConsoleCommands(pre)
    } else if (isBashBlock) {
        code = extractBashCommands(pre.textContent)
    } else {
        code = pre.textContent
    }

    navigator.clipboard.writeText(code).then(function () {
        const originalText = button.textContent
        button.textContent = 'Copied!'
        button.classList.add('copied')

        setTimeout(function () {
            button.textContent = originalText
            button.classList.remove('copied')
        }, 2000)
    }).catch(function (err) {
        console.error('Failed to copy code:', err)
        button.textContent = 'Failed'
        setTimeout(function () {
            button.textContent = 'Copy'
        }, 2000)
    })
}

function extractConsoleCommands(pre) {
    // In Pygments-highlighted console blocks:
    // - Prompts are in <span class="gp">
    // - Output is in <span class="go">
    // - Commands are everything else
    const preClone = pre.cloneNode(true)

    preClone.querySelectorAll('span.gp').forEach(function (span) { span.remove() })
    preClone.querySelectorAll('span.go').forEach(function (span) { span.remove() })

    const lines = preClone.textContent.split('\n')
        .map(function (line) { return line.trim() })
        .filter(function (line) { return line.length > 0 })

    return lines.join('\n')
}

function extractBashCommands(text) {
    const commandLines = []

    text.split('\n').forEach(function (line) {
        if (line.trim().startsWith('$')) {
            const command = line.replace(/^\s*\$\s*/, '')
            if (command.trim()) {
                commandLines.push(command)
            }
        } else if (line.trim().startsWith('#')) {
            commandLines.push(line.trim())
        }
        // Skip output lines
    })

    return commandLines.join('\n')
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addCopyButtons)
} else {
    addCopyButtons()
}
