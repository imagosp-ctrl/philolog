/**
 * ExploreAnotherTool Component
 * 
 * A reusable navigation component that displays circular links to other tools.
 * Automatically filters out the current page's tool from the display.
 * 
 * Usage: Include this script at the bottom of any feature page (not landing page).
 * The component will automatically inject itself after the main content container.
 */

(function() {
  'use strict';

  // ============================================
  // TOOL REGISTRY
  // Colors are 80% lightened versions of landing page tool buttons
  // ============================================
  const tools = [
    { name: 'Guided Reader', route: 'guided-reader.html', label: ['Guided', 'Reader'], color: '#dfeeff', hoverColor: '#c7e0ff' },
    { name: 'Psalms', route: 'psalms.html', label: ['Psalms'], color: '#b8d4f8', hoverColor: '#9ec4f4' },
    { name: 'Memory', route: 'memory.html', label: ['Memory'], color: '#d3e3fb', hoverColor: '#bdd4f7' },
    { name: 'Memory Deck', route: 'memory-deck.html', label: ['Memory', 'Deck'], color: '#c7deff', hoverColor: '#aed0ff' },
    { name: 'Lexicon', route: 'lexicon.html', label: ['Lexicon'], color: '#a8c8f0', hoverColor: '#8fb8eb' }
  ];

  // ============================================
  // ROUTE DETECTION
  // ============================================
  function getCurrentRoute() {
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
    return filename;
  }

  function getAvailableTools() {
    const currentRoute = getCurrentRoute();
    return tools.filter(tool => tool.route !== currentRoute);
  }

  // ============================================
  // COMPONENT STYLES
  // ============================================
  function injectStyles() {
    if (document.getElementById('explore-another-tool-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'explore-another-tool-styles';
    styles.textContent = `
      /* ExploreAnotherTool Component Styles */
      
      /* Wrapper section - solid white background, no bleed */
      .explore-another-tool-wrapper {
        position: relative;
        z-index: 2;
        background: #ffffff;
        padding: 56px 0 64px 0;
      }

      .explore-another-tool {
        max-width: 1140px;
        margin: 0 auto;
        padding: 0 48px;
      }

      .explore-another-tool__heading {
        font-family: 'Lora', serif;
        font-size: 1.35rem;
        font-weight: 500;
        color: #374151;
        margin: 0 0 32px 0;
        text-align: center;
        letter-spacing: 0.01em;
      }

      .explore-another-tool__grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 24px;
      }

      /* Circular tool buttons - base styles */
      .explore-another-tool__button {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        border: none;
        border-radius: 50%;
        width: 104px;
        height: 104px;
        transition: background 150ms ease-out;
        cursor: pointer;
      }

      .explore-another-tool__button-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        color: #1e3a5f;
        text-align: center;
        line-height: 1.25;
        display: flex;
        flex-direction: column;
        gap: 1px;
      }

      /* Responsive: Tablet */
      @media (max-width: 900px) {
        .explore-another-tool-wrapper {
          padding: 48px 0 56px 0;
        }

        .explore-another-tool {
          padding: 0 24px;
        }

        .explore-another-tool__button {
          width: 90px;
          height: 90px;
        }

        .explore-another-tool__button-text {
          font-size: 0.75rem;
        }

        .explore-another-tool__grid {
          gap: 20px;
        }
      }

      /* Responsive: Mobile */
      @media (max-width: 640px) {
        .explore-another-tool-wrapper {
          padding: 40px 0 48px 0;
        }

        .explore-another-tool {
          padding: 0 16px;
        }

        .explore-another-tool__heading {
          font-size: 1.2rem;
          margin-bottom: 24px;
        }

        .explore-another-tool__button {
          width: 78px;
          height: 78px;
        }

        .explore-another-tool__button-text {
          font-size: 0.7rem;
        }

        .explore-another-tool__grid {
          gap: 16px;
        }
      }

      /* Responsive: Very narrow screens */
      @media (max-width: 360px) {
        .explore-another-tool__button {
          width: 72px;
          height: 72px;
        }

        .explore-another-tool__button-text {
          font-size: 0.65rem;
        }

        .explore-another-tool__grid {
          gap: 12px;
        }
      }
    `;
    document.head.appendChild(styles);
  }

  // ============================================
  // COMPONENT RENDER
  // ============================================
  function createComponent() {
    const availableTools = getAvailableTools();
    
    // Don't render if no tools available (shouldn't happen)
    if (availableTools.length === 0) return null;

    // Outer wrapper for solid white background
    const wrapper = document.createElement('div');
    wrapper.className = 'explore-another-tool-wrapper';

    const container = document.createElement('div');
    container.className = 'explore-another-tool';

    // Heading
    const heading = document.createElement('h2');
    heading.className = 'explore-another-tool__heading';
    heading.textContent = 'Next:';
    container.appendChild(heading);

    // Button grid
    const grid = document.createElement('div');
    grid.className = 'explore-another-tool__grid';

    availableTools.forEach(tool => {
      const button = document.createElement('a');
      button.href = tool.route;
      button.className = 'explore-another-tool__button';
      
      // Apply individual tool color
      button.style.background = tool.color;
      
      // Add hover effect via event listeners
      button.addEventListener('mouseenter', () => {
        button.style.background = tool.hoverColor;
      });
      button.addEventListener('mouseleave', () => {
        button.style.background = tool.color;
      });

      const textContainer = document.createElement('span');
      textContainer.className = 'explore-another-tool__button-text';

      // Stack all labels vertically
      tool.label.forEach(word => {
        const span = document.createElement('span');
        span.textContent = word;
        textContainer.appendChild(span);
      });

      button.appendChild(textContainer);
      grid.appendChild(button);
    });

    container.appendChild(grid);
    wrapper.appendChild(container);
    return wrapper;
  }

  // ============================================
  // INJECTION LOGIC
  // ============================================
  function findInsertionPoint() {
    // Insert after framed-section (outside of it, on white background)
    const framedSection = document.querySelector('.framed-section');
    if (framedSection) {
      return { element: framedSection, position: 'afterend' };
    }

    // Lexicon uses lexicon-container
    const lexiconContainer = document.querySelector('.lexicon-container');
    if (lexiconContainer) {
      return { element: lexiconContainer, position: 'afterend' };
    }

    // Fallback: insert before first script tag in body
    const firstScript = document.querySelector('body > script');
    if (firstScript) {
      return { element: firstScript, position: 'beforebegin' };
    }

    return null;
  }

  function inject() {
    // Don't inject on landing page
    const currentRoute = getCurrentRoute();
    if (currentRoute === 'index.html' || currentRoute === '') {
      return;
    }

    // Check if already injected
    if (document.querySelector('.explore-another-tool')) {
      return;
    }

    // Inject styles
    injectStyles();

    // Create component
    const component = createComponent();
    if (!component) return;

    // Find insertion point and inject
    const insertPoint = findInsertionPoint();
    if (insertPoint) {
      insertPoint.element.insertAdjacentElement(insertPoint.position, component);
    }
  }

  // ============================================
  // INITIALIZATION
  // ============================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }

})();
